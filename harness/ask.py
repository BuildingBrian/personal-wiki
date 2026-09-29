"""Ask mode: the RAG workflow. Retrieve passages, build one prompt, call local Gemma, check the citations."""
import re
import sys

from . import config, evidence, index, model
from .textutil import numbers

REFUSAL = "Insufficient evidence: the wiki sources do not contain this information."
CITATION = r"\[(\d+(?:\s*,\s*\d+)*)\]"          # [1] and [1, 2]


def build_messages(question, hits):
    rules = (config.PROMPTS / "wiki-instructions.md").read_text(encoding="utf-8")
    shown = "\n\n".join(f"[{h['rank']}] ({h['source']} › {h['section']})\n{h['text']}" for h in hits)
    user = (f"QUESTION: {question}\n\nPASSAGES\n{shown}\n\nQUESTION (again): {question}\n\n"
            "Answer from the passages with citations like [1], or reply INSUFFICIENT EVIDENCE.")
    return [{"role": "system", "content": rules}, {"role": "user", "content": user}]


def tidy(reply):
    """A small model sometimes copies a table out of a passage before answering. The answer shown is the prose;
    the untouched reply is kept in the evidence record as raw_model_reply."""
    lines = [l for l in reply.splitlines() if not l.lstrip().startswith("|")]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()


def check_citations(answer, hits):
    """The harness does not trust the model's citations. It checks that every cited number is a passage that was
    actually retrieved, and that every figure in the answer appears in a cited passage."""
    groups = re.findall(CITATION, answer)
    cited = sorted({int(n) for group in groups for n in re.findall(r"\d+", group)})
    valid = [n for n in cited if 1 <= n <= len(hits)]
    cited_text = " ".join(hits[n - 1]["text"] for n in valid)
    figures = numbers(re.sub(CITATION, "", answer))
    unsupported = sorted(f for f in figures if f not in numbers(cited_text))
    return {"cited": cited, "valid_citations": valid, "invalid_citations": [n for n in cited if n not in valid],
            "figures_in_answer": sorted(figures), "figures_not_in_cited_passages": unsupported}


def run(question, k=config.TOP_K, out=None, quiet=False):
    out = out or sys.stdout
    retrieved = index.search(question, k)
    hits = retrieved["hits"]
    record = {"mode": "ask", "question": question, "uses_chat_history": False,
              "retrieval": {"method": "BM25 keyword index over vault/raw", "top_k": k,
                            "query_terms": retrieved["query_terms"],
                            "terms_not_in_index": retrieved["terms_not_in_index"],
                            "passages": [{key: h[key] for key in ("rank", "id", "path", "section", "lines", "score",
                                                                  "matched_terms", "text")} for h in hits]}}
    if not hits:
        record.update(status="insufficient_evidence", reason="retrieval returned no passage", raw_model_reply=None,
                      answer=REFUSAL, citation_check=None, model_stats=None)
    else:
        reply, stats = model.chat(build_messages(question, hits), max_tokens=220, temperature=0.1, purpose="ask")
        check = check_citations(reply, hits)
        if "INSUFFICIENT EVIDENCE" in reply.upper():
            status, answer, reason = "insufficient_evidence", REFUSAL, "the model found no answer in the passages"
        elif not check["valid_citations"]:
            status, answer = "insufficient_evidence", REFUSAL
            reason = "the model answered without citing any retrieved passage, so the harness withheld the answer"
        else:
            status, answer, reason = "answered", tidy(reply), None
        record.update(status=status, reason=reason, raw_model_reply=reply, answer=answer, citation_check=check,
                      model_stats=stats)
    record.update(evidence.stamp())          # taken after the call, so memory describes the loaded model
    if not quiet:
        show(record, out)
    return record


def show(record, out):
    print(f'ASK  "{record["question"]}"   (standalone: no chat history, no persona)', file=out)
    print(f"model: {record['model'].get('model')} ({record['model'].get('quantization')}) · execution: local · "
          f"network: {'connected' if record['internet_reachable'] else 'OFFLINE (Wi-Fi off, no network route)'}", file=out)
    print("\n" + record["answer"], file=out)
    passages = record["retrieval"]["passages"]
    check = record.get("citation_check") or {}
    if record["status"] == "answered":
        print("\nCitations:", file=out)
        for n in check["valid_citations"]:
            p = passages[n - 1]
            print(f"  [{n}] {p['path']}  ›  {p['section']}  (lines {p['lines'][0]}–{p['lines'][1]})", file=out)
        if check["invalid_citations"]:
            print(f"  WARNING: the answer cites {check['invalid_citations']}, which were not retrieved.", file=out)
        if check["figures_not_in_cited_passages"]:
            print(f"  WARNING: these figures are not in the cited passages: {check['figures_not_in_cited_passages']}", file=out)
    else:
        print(f"  reason: {record['reason']}", file=out)
        if passages:
            print("  closest passages that were searched:", file=out)
            for p in passages:
                print(f"    [{p['rank']}] {p['path']}  ›  {p['section']}", file=out)
    if record.get("model_stats"):
        s = record["model_stats"]
        print(f"\n({s['wall_seconds']} s · read {s['prompt_tokens']} tokens at {s['prompt_tokens_per_s']}/s · "
              f"wrote {s['output_tokens']} at {s['output_tokens_per_s']}/s · model memory {record['memory']['loaded_gb']} GB)", file=out)


def card(record, test=None, assessment=None):
    """Markdown evidence card for one ask-mode run."""
    lines = [f"# Evidence card: {test['id'] if test else 'ask'}", "",
             f"- **Mode:** ask (standalone, no chat history) · **Execution:** local",
             f"- **Recorded:** {record['recorded_at']} · **Network:** "
             + ("OFFLINE" if not record["internet_reachable"] else "connected")
             + f" (Wi-Fi {record['network']['wifi_power']}, default route {record['network']['default_route']}, "
             f"outside host answered {record['network']['outside_host_answered']})",
             f"- **Model:** {record['model'].get('model')} · {record['model'].get('parameter_size')} · "
             f"{record['model'].get('quantization')} · digest {record['model'].get('digest')} · "
             f"{record['model'].get('runtime')} {record['model'].get('runtime_version')}",
             f"- **Model memory:** {record['memory']['loaded_gb']} GB loaded, {record['memory']['processor']}", ""]
    lines += ["## Question", "", record["question"], ""]
    if test:
        lines += ["## Expected (written before the harness existed)", "",
                  f"- Kind: {test['kind']} — {test['design']}",
                  f"- Expected source: `{test['expected_source']}`" + (f" › {test['expected_section']}" if test.get("expected_section") else ""),
                  f"- Expected answer: {test['expected_answer']}", ""]
    lines += ["## Retrieved passages", "",
              f"Query terms: `{', '.join(record['retrieval']['query_terms'])}`"
              + (f" · not in any source: `{', '.join(record['retrieval']['terms_not_in_index'])}`" if record['retrieval']['terms_not_in_index'] else ""), ""]
    for p in record["retrieval"]["passages"]:
        lines += [f"### [{p['rank']}] `{p['path']}` › {p['section']} (lines {p['lines'][0]}–{p['lines'][1]})",
                  f"score {p['score']} · matched: {', '.join(p['matched_terms'])}", "",
                  "\n".join("> " + l for l in p["text"].splitlines()), ""]
    lines += ["## Actual answer", "", f"**Status:** {record['status']}"
              + (f" — {record['reason']}" if record.get("reason") else ""), "", record["answer"], ""]
    if record.get("raw_model_reply") is not None and record["raw_model_reply"] != record["answer"]:
        lines += ["Raw model reply before the harness applied its rules:", "", "```", record["raw_model_reply"], "```", ""]
    if record.get("citation_check"):
        c = record["citation_check"]
        lines += ["## Citation check (done by the harness)", "",
                  f"- Cited passages: {c['cited']} · valid: {c['valid_citations']} · not retrieved: {c['invalid_citations']}",
                  f"- Figures in the answer: {c['figures_in_answer']}",
                  f"- Figures missing from the cited passages: {c['figures_not_in_cited_passages']}", ""]
    if record.get("model_stats"):
        s = record["model_stats"]
        lines += ["## Timing", "", f"{s['wall_seconds']} s total · prompt {s['prompt_tokens']} tokens at "
                  f"{s['prompt_tokens_per_s']} tokens/s · answer {s['output_tokens']} tokens at {s['output_tokens_per_s']} tokens/s", ""]
    if test:
        expected_found = [p["rank"] for p in record["retrieval"]["passages"]
                          if test.get("expected_source") and p["path"] == test["expected_source"]
                          and all(s.lower() in p["text"].lower() for s in test.get("expected_passage_contains", []))]
        lines += ["## Automatic checks", "",
                  f"- Expected passage retrieved at rank: {expected_found or 'NOT RETRIEVED'}"
                  if test["kind"] == "answerable" else "- Expected behavior: insufficient evidence", ""]
    lines += ["## My assessment", "", assessment or "_to be written after reading the cited passages_", ""]
    return "\n".join(lines)
