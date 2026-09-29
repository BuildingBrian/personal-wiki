"""Chat mode: a personal assistant with a persona and conversation context.

The harness, not the model, decides whether a turn needs the wiki. Casual turns and follow-ups go to the model with
the conversation only. Turns about the projects get retrieved passages attached, and the reply must cite them.
"""
import re
import sys
import time

from . import ask, config, index, model, search
from .textutil import terms

CAPABILITY = re.compile(r"(what can (we|you|i) do|what can you help|what (do|can) you do|who are you|what are you|"
                        r"how do you work|your capabilit|^\s*(hello|hi|hey|good (morning|afternoon|evening))\b)", re.I)
FOLLOW_UP = re.compile(r"^\s*(make (that|it|this)\b|shorten|shorter|longer|rewrite|rephrase|reword|try again|again\b|"
                       r"simplif|expand (that|it)|turn (that|it)|summari[sz]e (that|it)|same but|now (make|do|write)|"
                       r"thanks|thank you|ok\b|okay\b|great\b|nice\b|perfect\b|yes\b|no\b|sure\b)", re.I)
EXPLICIT = re.compile(r"\b(my (notes|wiki|sources|write-?ups?)|in (the|my) wiki|from (the|my) wiki|according to|"
                      r"look (it |that |this )?up|remind me|what (did|was|were|have|had) i\b|did i\b)", re.I)
MIN_SCORE, MIN_TERMS, MIN_COVERAGE = 7.0, 3, 0.6


def subjects(loaded_index):
    """Names a message can use for a project: taken from the source names, plus a few aliases."""
    names = {tuple(terms(re.sub(r"readme", "", source, flags=re.I))[:2])
             for source in {p["source"] for p in loaded_index["passages"]}}
    names |= {tuple(terms(alias)) for alias in config.CHAT_SUBJECT_ALIASES}
    return {n for n in names if n}


HELP = """Commands inside chat:
  /search <words>    show original passages from the sources (no model)
  /ask <question>    neutral standalone answer with citations (ignores this conversation)
  /sources           show the passages used for the last reply
  /save              save the last reply as a draft in outputs/ (never into the wiki)
  /help              this list
  /quit              leave chat
Anything else is conversation with Ledger."""


def decide(message, loaded_index):
    """Return (passages or None, reason). This is the retrieval decision the README documents."""
    if CAPABILITY.search(message):
        return None, "skipped: question about the assistant itself"
    if FOLLOW_UP.search(message):
        return None, "skipped: follow-up on the conversation"
    result = index.search(message, config.CHAT_TOP_K, loaded_index)
    hits = result["hits"]
    if not hits:
        return None, "skipped: no wiki passage shares a word with this message"
    best = hits[0]
    if EXPLICIT.search(message):
        return hits, f"looked up {len(hits)} passages: the message asks about my records"
    said = set(terms(message))
    named = [" ".join(name) for name in subjects(loaded_index) if set(name) <= said]
    if named:
        return hits, f"looked up {len(hits)} passages: the message names a project ({named[0]})"
    if len(best["matched_terms"]) >= MIN_TERMS and best["coverage"] >= MIN_COVERAGE and best["score"] >= MIN_SCORE:
        return hits, (f"looked up {len(hits)} passages: strong match with the sources "
                      f"(score {best['score']}, {int(best['coverage'] * 100)}% of the message's terms)")
    return None, f"skipped: weak match with the sources (best score {best['score']})"


def build_messages(message, history, hits):
    persona = (config.PROMPTS / "persona.md").read_text(encoding="utf-8")
    if hits:
        shown = "\n\n".join(f"[{h['rank']}] ({h['source']} › {h['section']})\n{h['text']}" for h in hits)
        turn = (f"WIKI PASSAGES looked up for this message:\n{shown}\n\n"
                "Use these passages for any fact about Brian's projects and cite them like [1]. "
                "Label your own ideas with \"Suggestion:\".\n\n" f"Brian: {message}")
    else:
        turn = ("(No wiki passages were looked up for this message. Do not state facts about Brian's projects "
                f"from memory.)\n\nBrian: {message}")
    return [{"role": "system", "content": persona}] + history[-config.CHAT_HISTORY_TURNS:] + [{"role": "user", "content": turn}]


def run(script=None, transcript=None, out=None):
    out = out or sys.stdout
    try:
        loaded_index = index.load()
    except index.IndexMissing as exc:
        print(str(exc), file=out)
        return 1
    print(model.banner(), file=out)
    print("Ledger: your project assistant. I run on this laptop only. Type /help for commands, /quit to leave.\n", file=out)
    history, log, last_hits, last_reply = [], [], [], ""
    scripted = list(script) if script is not None else None
    while True:
        if scripted is not None:
            if not scripted:
                break
            message = scripted.pop(0).strip()
            print(f"You: {message}", file=out)
        else:
            try:
                message = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                print(file=out)
                break
        if not message:
            continue
        if message in ("/quit", "/exit"):
            break
        if message == "/help":
            print(HELP + "\n", file=out)
            continue
        if message.startswith("/search"):
            search.run(message[len("/search"):].strip() or "?", out=out)
            print(file=out)
            log.append({"you": message, "harness": "command: search (no model call)", "reply": None})
            continue
        if message.startswith("/ask"):
            record = ask.run(message[len("/ask"):].strip(), out=out)
            print(file=out)
            log.append({"you": message, "harness": "command: ask (standalone, conversation not used)",
                        "reply": record["answer"]})
            continue
        if message == "/sources":
            if not last_hits:
                print("  No passages were looked up for the last reply.\n", file=out)
            for h in last_hits:
                print(f"  [{h['rank']}] {h['path']}  ›  {h['section']}  (lines {h['lines'][0]}–{h['lines'][1]})", file=out)
            print(file=out)
            continue
        if message == "/save":
            if last_reply:
                config.OUTPUTS.mkdir(parents=True, exist_ok=True)
                path = config.OUTPUTS / f"chat-draft-{time.strftime('%Y%m%d-%H%M%S')}.md"
                path.write_text("<!-- Generated draft from chat. Not source evidence. -->\n\n" + last_reply + "\n", encoding="utf-8")
                print(f"  saved to {path.relative_to(config.ROOT)} (a draft, kept outside the wiki)\n", file=out)
            continue

        hits, reason = decide(message, loaded_index)
        print(f"  [harness] wiki lookup {reason}", file=out)
        print("Ledger: ", end="", file=out)
        out.flush()
        try:
            reply, stats = model.chat(build_messages(message, history, hits), max_tokens=260, temperature=0.5,
                                      purpose="chat", stream_to=out)
        except model.ModelUnavailable as exc:
            print(f"\n  {exc}\n", file=out)
            continue
        print(file=out)
        if hits:
            cited = sorted({int(n) for group in re.findall(ask.CITATION, reply) for n in re.findall(r"\d+", group)
                            if 1 <= int(n) <= len(hits)})
            for n in cited:
                h = hits[n - 1]
                print(f"  [{n}] {h['path']}  ›  {h['section']}  (lines {h['lines'][0]}–{h['lines'][1]})", file=out)
            if not cited:
                print("  [harness] the reply cites no passage: treat any project fact in it as unverified", file=out)
        print(f"  ({stats['wall_seconds']} s)\n", file=out)
        history += [{"role": "user", "content": message}, {"role": "assistant", "content": reply}]
        last_hits, last_reply = hits or [], reply
        log.append({"you": message, "harness": reason, "reply": reply, "seconds": stats["wall_seconds"],
                    "passages": [f"{h['path']} › {h['section']}" for h in (hits or [])]})
    if transcript:
        save_transcript(transcript, log)
        print(f"transcript saved to {transcript}", file=out)
    return 0


def save_transcript(path, log):
    from . import evidence
    stamp = evidence.stamp()
    lines = ["# Chat transcript", "",
             f"- **Mode:** chat · **Execution:** local · **Recorded:** {stamp['recorded_at']} · "
             f"**Network:** {'OFFLINE' if not stamp['internet_reachable'] else 'connected'} "
             f"(Wi-Fi {stamp['network']['wifi_power']}, default route {stamp['network']['default_route']})",
             f"- **Model:** {stamp['model'].get('model')} {stamp['model'].get('quantization')} · "
             f"{stamp['model'].get('runtime')} {stamp['model'].get('runtime_version')}", ""]
    for turn in log:
        lines += [f"**You:** {turn['you']}", "", f"`harness: {turn['harness']}`", ""]
        for p in turn.get("passages", []):
            lines.append(f"- passage: `{p}`")
        if turn.get("reply"):
            lines += ["", "**Ledger:** " + turn["reply"].replace("\n", "\n\n"), ""]
        if turn.get("seconds"):
            lines += [f"_{turn['seconds']} s_", ""]
        lines.append("---\n")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
