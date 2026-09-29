"""The command-line interface. It only parses the command and hands it to one mode of the harness."""
import argparse
import json
import sys
from pathlib import Path

from . import ask, chat, config, evidence, index, ingest, model, search

OVERVIEW = """Personal wiki: talk to your own notes with a local Gemma model. Works offline.

Commands
  ./wiki ingest vault/raw          read the sources, rebuild the search index, draft linked wiki notes
  ./wiki search "row level security"   show original passages and where they come from (no model)
  ./wiki ask "Where is ...?"       neutral standalone answer with citations, or "insufficient evidence"
  ./wiki chat                      personal assistant with conversation context
  ./wiki status                    model, runtime, device and index details
  ./wiki test                      run the four ask tests and the mode checks, save evidence
  ./wiki help                      this page

Required inputs
  Sources   .md or .txt files in vault/raw/ (never modified)
  Model     a Gemma model in a local Ollama runtime (default gemma4:e2b); download it while online:
            ollama pull gemma4:e2b
Configuration
  harness/config.py                passage size, top-k, context size, folders
  prompts/wiki-instructions.md     research rules for ask
  prompts/persona.md               the assistant's voice and capabilities for chat
  WIKI_MODEL, WIKI_OLLAMA_URL      environment overrides
Execution
  --mode local is the default and the only mode implemented. Nothing is sent off this machine."""


def build_parser():
    parser = argparse.ArgumentParser(prog="wiki", description=OVERVIEW, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", metavar="command")
    p = sub.add_parser("ingest", help="read sources, rebuild the index, draft wiki notes")
    p.add_argument("paths", nargs="*", default=[], help="a source file or folder inside vault/raw (default: all)")
    p.add_argument("--force", action="store_true", help="draft notes again even if the source is unchanged")
    p.add_argument("--replan", action="store_true", help="ask the model for a new note plan (changes note names)")
    p = sub.add_parser("search", help="show matching original passages (no model)")
    p.add_argument("query")
    p.add_argument("-k", type=int, default=config.TOP_K + 1, help="how many passages to show")
    p = sub.add_parser("ask", help="standalone factual answer with citations")
    p.add_argument("question")
    p.add_argument("--mode", choices=["local", "online"], default="local")
    p.add_argument("-k", type=int, default=config.TOP_K, help="how many passages to give the model")
    p.add_argument("--save", metavar="NAME", help="save an evidence card under evidence/ask/NAME")
    p = sub.add_parser("chat", help="personal assistant with conversation context")
    p.add_argument("--mode", choices=["local", "online"], default="local")
    p.add_argument("--script", type=Path, help="read the turns from a file, one per line (for repeatable checks)")
    p.add_argument("--transcript", type=Path, help="save the conversation to this Markdown file")
    p = sub.add_parser("status", help="model, runtime, device and index details")
    p.add_argument("--save", action="store_true", help="write evidence/model_card.json")
    p = sub.add_parser("test", help="run the four ask tests and the mode checks")
    p.add_argument("--out", type=Path, default=config.EVIDENCE, help="where to save the evidence")
    p.add_argument("--only", choices=["ask", "modes"], help="run one half only")
    sub.add_parser("help", help="show this page")
    return parser


def status(save=False):
    info = {"device": evidence.device(), **evidence.stamp()}
    try:
        loaded = index.load()
        info["index"] = {"passages": len(loaded["passages"]), "method": loaded["method"], "built_at": loaded["built_at"],
                         "sources": len(loaded["sources"]), "target_passage_words": loaded["passage_words"]}
    except index.IndexMissing as exc:
        info["index"] = {"error": str(exc)}
    print(json.dumps(info, indent=2, ensure_ascii=False))
    if save:
        config.EVIDENCE.mkdir(parents=True, exist_ok=True)
        (config.EVIDENCE / "model_card.json").write_text(json.dumps(info, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"\nsaved to {config.EVIDENCE / 'model_card.json'}")


def run_tests(out_dir, only=None):
    tests = json.loads((config.ROOT / "tests" / "questions.json").read_text(encoding="utf-8"))
    summary = []
    if only in (None, "ask"):
        for test in tests["tests"]:
            print("=" * 100)
            record = ask.run(test["question"])
            record["test"] = test
            found = [p["rank"] for p in record["retrieval"]["passages"]
                     if test["expected_source"] and p["path"] == test["expected_source"]
                     and all(s.lower() in p["text"].lower() for s in test["expected_passage_contains"])]
            record["expected_passage_rank"] = found
            evidence.save(out_dir / "ask", test["id"], record, ask.card(record, test))
            summary.append((test["id"], test["kind"], record["status"], found))
            print()
        print("=" * 100)
        for row in summary:
            print(f"  {row[0]}  {row[1]:<12} status={row[2]:<22} expected passage at rank {row[3] or '-'}")
        print(f"  evidence cards saved in {out_dir / 'ask'}")
    if only in (None, "modes"):
        checks = tests["mode_checks"]
        modes = out_dir / "mode-checks"
        modes.mkdir(parents=True, exist_ok=True)
        print("=" * 100 + "\nMODE CHECK 1: chat capabilities and follow-up\n")
        chat.run(script=checks["chat_capabilities"] + checks["chat_followup"], transcript=modes / "chat-capabilities-and-followup.md")
        print("=" * 100 + "\nMODE CHECK 2: search returns passages and no generated answer\n")
        with open(modes / "search-check.txt", "w", encoding="utf-8") as fh:
            fh.write(model.banner() + "\n\n")
            search.run(checks["search"], out=fh)
        print((modes / "search-check.txt").read_text(encoding="utf-8"))
        print("=" * 100 + "\nMODE CHECK 3: a claim made only in chat is not evidence for ask\n")
        sep = checks["ask_chat_separation"]
        chat.run(script=[sep["chat_only_claim"]], transcript=modes / "separation-chat-side.md")
        record = ask.run(sep["ask_question"])
        evidence.save(modes, "separation-ask-side", record, ask.card(record))
        print(f"\n  mode check evidence saved in {modes}")
    return 0


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command in (None, "help"):
        print(OVERVIEW)
        return 0
    if getattr(args, "mode", "local") == "online":
        print("Online mode is an optional extension and is not implemented. This project is local only: "
              "leave out --mode or use --mode local.")
        return 2
    try:
        if args.command == "ingest":
            print(model.banner())
            result = ingest.run(args.paths, force=args.force, replan=args.replan)
            return 1 if "error" in result else 0
        if args.command == "search":
            search.run(args.query, args.k)
            return 0
        if args.command == "ask":
            record = ask.run(args.question, args.k)
            if args.save:
                path = evidence.save(config.EVIDENCE / "ask", args.save, record, ask.card(record))
                print(f"\nevidence card saved to {path}")
            return 0
        if args.command == "chat":
            script = None
            if args.script:
                if not args.script.exists():
                    print(f"Script file not found: {args.script}")
                    return 2
                script = [l for l in args.script.read_text(encoding="utf-8").splitlines() if l.strip()]
            return chat.run(script=script, transcript=args.transcript)
        if args.command == "status":
            status(args.save)
            return 0
        if args.command == "test":
            return run_tests(args.out, args.only)
    except index.IndexMissing as exc:
        print(exc)
        return 2
    except model.ModelUnavailable as exc:
        print(f"Local model unavailable.\n  {exc}")
        return 3
    except FileNotFoundError as exc:
        print(f"Missing file: {exc.filename}\n  Run ./wiki help to see the required inputs.")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
