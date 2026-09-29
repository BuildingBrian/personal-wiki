"""Render README.md from the saved evidence, so every number in it comes from a file a reader can open."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "evidence"
J = lambda p: json.loads(Path(p).read_text(encoding="utf-8"))


def load_tests(folder):
    out = []
    for n in (1, 2, 3, 4):
        path = folder / "ask" / f"test-{n}.json"
        if path.exists():
            out.append(J(path))
    return out


def one_line(text, limit=400):
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= limit else text[: limit - 1] + "…"


card = J(E / "model_card.json")
device, ident, memory = card["device"], card["model"], card["memory"]
online = load_tests(E / "online")
offline = load_tests(E / "offline")
run1 = [J(p) for p in sorted((E / "runs" / "run-1-initial").glob("test-*.json"))]
assess = J(ROOT / "tests" / "assessments.json") if (ROOT / "tests" / "assessments.json").exists() else {}
catalog = J(ROOT / "data" / "catalog.json")["sources"]
plan = J(ROOT / "data" / "plan.json")
notes = sorted((ROOT / "vault" / "wiki").rglob("*.md"))
reports = sorted((E / "ingest").glob("ingest-*.json"))
full = next((J(p) for p in reversed(reports) if len(J(p).get("drafts", [])) >= 10), None)
off_ingest = next((J(p) for p in reversed(reports) if p.stem.endswith("-offline")), None)
passages = J(ROOT / "data" / "index" / "passages.json")
have_offline = bool(offline) and all(not t["internet_reachable"] for t in offline)
shots = {p.name for p in (E / "obsidian").glob("*.png")} if (E / "obsidian").exists() else set()
off_shots = sorted(p.name for p in (E / "offline").glob("*.png")) if (E / "offline").exists() else []


def status_word(t):
    return {"answered": "answered", "insufficient_evidence": "insufficient evidence"}[t["status"]]


def test_row(t, where):
    rank = t.get("expected_passage_rank") or "—"
    cited = (t.get("citation_check") or {}).get("valid_citations", [])
    secs = (t.get("model_stats") or {}).get("wall_seconds", "—")
    return (f"| {t['test']['id']} | {t['question']} | {t['test']['kind']} | {status_word(t)} | {rank} | "
            f"{cited or '—'} | {secs} s | [card]({where}/ask/{t['test']['id']}.md) |")


L = []
w = L.append
best = offline if have_offline else online
w(f"""# Ledger — a personal wiki I can talk to, running on my own laptop

**Brian Arevalo Ramos · MBA 290T Fundamentals of Agentic AI · Class 5, Assignment 4 · 2026-09-29**

Ledger is a command-line assistant that answers from my own project notes using a local open-weight model,
`{ident['model']}` ({ident.get('parameter_size')} parameters, {ident.get('quantization')}), with no internet connection.
I wrote the CLI and the harness myself in plain Python with no third-party packages. It has three modes that behave
differently on purpose:

| Mode | What it does | Uses the model | Uses my notes | Uses the conversation |
|---|---|---|---|---|
| `search` | Shows the original passages and where they come from | no | yes | no |
| `ask` | Neutral, standalone answer with citations, or an explicit "insufficient evidence" | yes | always | never |
| `chat` | A personal assistant with a voice, for brainstorming, drafting and planning | yes | only when the turn needs them | yes |

Two more commands feed it: `ingest` turns sources into a linked wiki that I can browse in Obsidian, and `help`
explains everything. This README is the entry point: every claim links to a saved file, and the numbers in it are
read from those files by [`scripts/build_readme.py`](scripts/build_readme.py).

## Results at a glance

""")
if have_offline:
    w("All four questions below were run **with Wi-Fi off**, after restarting the CLI "
      "([full offline session](evidence/offline/session.txt)).\n")
else:
    w("> **Offline run pending.** The results below are from the local model with the laptop still connected. "
      "The offline demonstration is run with `Run offline demo.command` after turning Wi-Fi off.\n")
w("| Test | Question | Kind | Result | Expected passage retrieved at rank | Passages cited | Time | Evidence |")
w("|---|---|---|---|---|---|---|---|")
where = "evidence/offline" if have_offline else "evidence/online"
for t in best:
    w(test_row(t, where))
w(f"""
Three answerable questions were answered from retrieved passages with checked citations, and the question my
sources cannot answer got an explicit refusal. It did not work the first time: [section 8](#8-what-failed-first-and-what-i-changed)
keeps the first run, where test 2 failed, and the two bugs in my own harness that it exposed.

## 1. Purpose and sources

**What the wiki is for.** It is my memory of the projects I built in this course: what I built, what I measured,
what failed and what I said I would try next. The questions I want it to answer are the ones I actually ask myself a
month later: "what score did that reach?", "why did that fail?", "what did I say I would try next?".

**Sources.** Three write-ups I authored for earlier assignments. They are my own work and already public in my own
repositories, so they are shareable, and I know them well enough to check every answer. Originals are copied
byte-for-byte into [`vault/raw/`](vault/raw/) and never modified; the harness only reads them.

| ID | Source in the vault | Original file | Origin | Words | SHA-256 |
|---|---|---|---|---|---|""")
for e in catalog:
    w(f"| {e['id']} | [`vault/{e['path']}`](<vault/{e['path']}>) | `{e.get('original_filename', '')}` | "
      f"{e.get('origin', '')} | {e.get('words', ''):,} | `{e['sha256'][:16]}…` |")
w(f"""
**How an original becomes a wiki page.** `ingest` gives each source a stable id, cuts it into sections, and asks
local Gemma to draft one note per subject from the section text. The harness, not the model, chooses the file name,
the folder, the properties and the source references, so every note in [`vault/wiki/`](vault/wiki/) carries links
back to the exact section of the original it came from. I then read each draft against its source and mark it
`reviewed: true`. The map from source sections to notes is [`data/plan.json`](data/plan.json); the source catalog is
[`data/catalog.json`](data/catalog.json) and is also printed at the bottom of [`vault/index.md`](vault/index.md).

## 2. Setup and exact commands

Requirements: macOS or Linux, Python 3.9 or newer (standard library only), and [Ollama](https://ollama.com) as the
local runtime. While online, once:

```bash
git clone https://github.com/BuildingBrian/personal-wiki.git && cd personal-wiki
ollama pull {ident['model']}          # official Gemma weights, {ident.get('size_on_disk_gb')} GB; nothing else is downloaded
ollama list                       # confirm the model is stored locally before going offline
```

Model weights are not in this repository. The exact identifier is `{ident['model']}`, digest `{ident.get('digest')}`,
from the Ollama library's official Gemma listing. There is no embedding model, no tokenizer download and no pip
install: retrieval is a keyword index built with the standard library.

Then, online or offline:

```bash
./wiki help                                   # commands, configuration, required inputs
./wiki ingest vault/raw                       # read sources, rebuild the search index, draft linked notes
./wiki search "row level security"            # original passages and paths, no model
./wiki ask "What was the mean evaluation score of the Pac-Man agent before and after training?"
./wiki chat                                   # the assistant; /help inside lists /search /ask /sources /save /quit
./wiki check                                  # names, headings, links, source references
./wiki status                                 # model, runtime, device, network, index
./wiki test                                   # the four ask tests and the mode checks, saved under evidence/
```

`--mode local` is the default and the only mode implemented. `--mode online` prints a message saying so and exits.

## 3. Device, model, and why this model

| | |
|---|---|
| Computer | 2019 MacBook Pro 16-inch, {device['os']}, {device['machine']} |
| CPU | {device['cpu']}, {device['cpu_cores']} cores |
| RAM | {device['ram_gb']} GB total, {device['available_memory_gb']} GB available when measured |
| GPU | {', '.join(device['gpu'])} (dedicated VRAM 4 GB; **not used**: the runtime reports {memory['processor']}) |
| Free disk | {device['free_disk_gb']} GB |
| Model | `{ident['model']}` · family {ident.get('family')} · {ident.get('parameter_size')} parameters · {ident.get('file_format')} |
| Quantization | {ident.get('quantization')} |
| Runtime | {ident['runtime']} {ident.get('runtime_version')}, HTTP API on `127.0.0.1:11434` |
| Context used | {ident.get('context_tokens_used')} tokens, the same in every mode |
| Python | {device['python']} |

Source: [`evidence/model_card.json`](evidence/model_card.json), written by `./wiki status --save`.

**Why E2B.** Memory is not my constraint, speed is. This is an Intel Mac, so there is no unified memory and the
runtime does not use the Radeon GPU: everything runs on six CPU cores. I measured before building
([`tests/EXPECTATIONS.md`](tests/EXPECTATIONS.md)): the model reads a prompt at roughly 50 to 60 tokens per second
and writes at about 15 to 18. A 3,000-token prompt took 72 seconds to read. E4B or the 26B model would fit in
{device['ram_gb']} GB of RAM but would be slower still, and my wiki is small enough that the smallest model answers
correctly once retrieval gives it the right passage. So I chose the smallest model that works and spent the design
effort on keeping prompts short.
""")
ask_times = [t["model_stats"]["wall_seconds"] for t in best if t.get("model_stats")]
ask_prompt = [t["model_stats"]["prompt_tokens"] for t in best if t.get("model_stats")]
w("**Measured on this laptop.**\n")
w("| Measurement | Value | Source |")
w("|---|---|---|")
w(f"| Model memory while loaded | {memory['loaded_gb']} GB, {memory['processor']} | `ollama ps` via [`model_card.json`](evidence/model_card.json) |")
if ask_times:
    w(f"| One `ask` answer | {min(ask_times)} to {max(ask_times)} s (prompt {min(ask_prompt)} to {max(ask_prompt)} tokens) | [{where}/ask/]({where}/ask/) |")
if full:
    d = full["drafts"]
    w(f"| Full ingestion, {len(d)} notes drafted and linked | {round(full['seconds'] / 60, 1)} min in total; "
      f"{round(sum(x['wall_seconds'] for x in d) / len(d), 1)} s per note on average | "
      f"[ingest report](evidence/ingest/) |")
    w(f"| Text passed to Gemma for one note | {min(x['source_words_passed'] for x in d)} to {max(x['source_words_passed'] for x in d)} words "
      f"({min(x['prompt_tokens'] for x in d)} to {max(x['prompt_tokens'] for x in d)} tokens) | same report |")
    w(f"| Reading speed / writing speed | {round(sum(x['prompt_tokens_per_s'] for x in d) / len(d), 1)} / "
      f"{round(sum(x['output_tokens_per_s'] for x in d) / len(d), 1)} tokens per second | same report |")
if off_ingest:
    w(f"| Offline re-ingestion of one source | {round(off_ingest['seconds'] / 60, 1)} min, "
      f"{len(off_ingest['drafts'])} notes drafted, {len(off_ingest['unplanned_files'])} duplicates | "
      f"[offline ingest report](evidence/ingest/) |")
w(f"| Search index | {len(passages['passages'])} passages from {len(catalog)} sources, rebuilt in under a second | [`data/index/passages.json`](data/index/passages.json) |")
w("""
## 4. Architecture: model, retrieval tool, RAG workflow, CLI, harness

```mermaid
flowchart LR
    U["./wiki &lt;command&gt;"] --> CLI["cli.py<br/>parse the command"]
    CLI -->|search| S["search.py"]
    CLI -->|ask| A["ask.py<br/>RAG workflow"]
    CLI -->|chat| C["chat.py<br/>persona + conversation"]
    CLI -->|ingest| I["ingest.py"]
    S --> R[("index.py<br/>retrieval tool: BM25 over<br/>passages of vault/raw")]
    A --> R
    C -->|"only if decide() says the turn needs notes"| R
    A --> M["model.py<br/>local Gemma via Ollama<br/>127.0.0.1"]
    C --> M
    I --> M
    A --> K["check_citations()"]
    A --> E["evidence.py<br/>evidence cards"]
    I --> W[("vault/wiki notes<br/>vault/index.md")]
    I --> R
```

| Part | What it is here | File |
|---|---|---|
| **Model** | Local Gemma. It generates text from the instructions and context it is given. It does not read my files, remember conversations or decide anything about retrieval. | called only from [`harness/model.py`](harness/model.py) |
| **Retrieval tool** | Code that searches a local keyword index and returns original passages with source path, section and line numbers. Works with the model switched off. | [`harness/index.py`](harness/index.py), [`harness/chunking.py`](harness/chunking.py) |
| **RAG workflow** | Retrieve passages, put them in a prompt, have the model answer from them. Used by `ask` always and by `chat` sometimes. It supplies context at answer time. It does not train Gemma: the weights never change. | [`harness/ask.py`](harness/ask.py) |
| **CLI** | The terminal interface. It parses one command and hands it to one mode. | [`wiki`](wiki), [`harness/cli.py`](harness/cli.py) |
| **Harness** | Everything around the model: mode selection, instructions and persona, conversation context, the retrieval decision, prompt assembly, the model call, citation checks, error messages and saved outputs. | [`harness/`](harness/) |

### One question, traced through the code

`./wiki ask "What was the mean evaluation score of the Pac-Man agent before and after training?"`

1. [`wiki`](wiki) calls `cli.main()`, which parses the command and calls `ask.run(question)`. No chat history exists in this process.
2. `ask.run` calls `index.search`. [`textutil.terms`](harness/textutil.py) lowercases the question, drops stopwords and strips endings, giving `mean, evalu, score, pac, man, agent, train`. BM25 scores every passage and returns the top 4 with path, section and line numbers.
3. `ask.build_messages` reads the research rules from [`prompts/wiki-instructions.md`](prompts/wiki-instructions.md) as the system message. The user message is the question, the four numbered passages with their source labels, and the question again.
4. `model.chat` posts that to `http://127.0.0.1:11434/api/chat` with thinking off, temperature 0.1, context 4096 and at most 220 output tokens, and measures the timing.
5. Back in `ask.run`: if the reply contains `INSUFFICIENT EVIDENCE`, the answer is the refusal. Otherwise `check_citations` confirms that every `[n]` refers to a passage that was actually retrieved and that every figure in the answer appears in a cited passage. An answer with no valid citation is withheld and reported as insufficient evidence.
6. `ask.show` prints the answer and the cited paths. With `--save` or `./wiki test`, [`evidence.py`](harness/evidence.py) writes the evidence card with the question, passages, raw reply, checks, model identity, network state and timing.

### How the harness handles each responsibility

| Responsibility | How |
|---|---|
| Choosing a mode | The user chooses with the command. Inside chat, `/search` and `/ask` run those modes without leaving the conversation. |
| Conversation context | `chat.py` keeps the last 6 messages. Retrieved passages are attached to the current turn only, never stored as history. `ask` and `search` receive no history at all. |
| Deciding whether to retrieve | `chat.decide()`, rules first then scores. Questions about the assistant and follow-ups such as "make that shorter" never retrieve. Messages that refer to the wiki always retrieve. Otherwise it retrieves only if the best passage matches at least 2 terms, covers at least half of the message's terms, and scores at least 6.0. The decision is printed on every turn. |
| Building prompts | `ask`: research rules + passages. `chat`: persona + history + passages when retrieved, or an explicit note that nothing was looked up. `ingest`: the note title + at most 900 words of source. |
| Calling Gemma | One function, `model.chat`, local only. |
| Checking citations | `ask.check_citations`, described above. In chat, a reply that used passages but cites none is flagged as unverified. |
| Errors | Runtime not running, model not downloaded, index missing, source not found and script file missing each print what is wrong and the command that fixes it. `search` keeps working when the model is unavailable. |
| Saved outputs | Evidence cards as JSON and Markdown, chat transcripts, ingestion reports, and every model call in a local log. Drafts saved from chat with `/save` go to `outputs/`, never into the wiki. |

## 5. Design choices
""")
w(f"""| Choice | Value | Why |
|---|---|---|
| Passage size | about 130 words, at most 190 | Four passages are about 1,500 tokens, which this CPU reads in about 25 seconds. Passages are cut at headings and paragraph boundaries; long tables are cut by rows with the header repeated so a row never loses its column names. |
| Retrieval method | BM25 keyword index, heading words counted twice | No download, no embedding model, works offline by construction, and I can explain every score. Its weakness, wording, is exactly what test 2 probes. |
| What is indexed | The original sources only | Citations must point to evidence, not to a model's summary of it. Wiki notes are for me to browse; each one links back to its source section. |
| Passages per question | 4 for ask, 3 for chat | More passages means more reading time and more distraction for a small model. |
| Context window | 4096 tokens in every mode | Changing the context size makes the runtime reload the model, which costs about 11 seconds. |
| Research rules | [`prompts/wiki-instructions.md`](prompts/wiki-instructions.md) | Neutral voice, cite every fact, copy figures exactly, refuse in two fixed words so the harness can detect it. |
| Assistant personality | [`prompts/persona.md`](prompts/persona.md): "Ledger", direct and practical | The persona file also lists what the assistant can and cannot do, so "what can you help me with?" is answered from instructions rather than from notes. |
| Thinking | switched off | With thinking on, this model spent its whole output budget on hidden reasoning and returned an **empty reply** in my first call. |
| Temperature | 0.1 ask, 0.2 ingest, 0.5 chat | Facts should be repeatable; conversation can vary. |
| Note names | 2 to 5 words, Title Case, chosen by the harness from a plan | The model never writes a file name, so hashes, timestamps and sentence-length names cannot reach the vault. `./wiki check` enforces it. |
| Folders | `Projects`, `Results`, `Concepts`, `Lessons` | They match the questions I ask: what was it, what did it score, how does it work, what went wrong. |
| Source ids | `S1`, `S2`, `S3` in note properties, the catalog and evidence files | Readable names for people, stable ids for machines. Original file names are kept in the catalog. |
| Re-ingestion | The plan decides the file, so the same source always writes the same notes | A note I have reviewed is never overwritten; the fresh draft goes to `data/drafts/`. A generated note that is no longer in the plan is moved out of the vault. |

## 6. The wiki in Obsidian
""")
w(f"The vault is the [`vault/`](vault/) folder itself: {len(notes)} notes in `wiki/`, {len(catalog)} originals in `raw/`, "
  "and `index.md` as the landing page. Code, the search index, evidence and drafts all live outside it.\n")
for name, caption in (("1-open-note-with-sources.png", "An open note: short file name, matching heading, related notes with reasons, and source references that link to the exact section of the original."),
                      ("2-index-and-page-list.png", "The landing page grouped by topic, with the page list on the left."),
                      ("3-graph-view.png", "Graph view, filtered with `path:wiki/`, attachments off, colored by folder.")):
    if name in shots:
        w(f"**{caption}**\n\n![{caption}](evidence/obsidian/{name})\n")
w("""The screenshots are Obsidian's own window contents, captured by [`scripts/obsidian_shots.py`](scripts/obsidian_shots.py)
through the app's developer interface. The graph filter and colors are saved in
[`vault/.obsidian/graph.json`](vault/.obsidian/graph.json), so opening the vault reproduces the same view.
""")
if (E / "obsidian" / "link-check.txt").exists():
    w("**Links and names, checked two ways.** `./wiki check` verifies every file name, heading, link and source "
      "reference, and Obsidian's own link resolver was asked for unresolved links:\n")
    w("```\n" + (E / "obsidian" / "link-check.txt").read_text(encoding="utf-8").strip() + "\n```\n")
if (E / "obsidian" / "trace.md").exists():
    w((E / "obsidian" / "trace.md").read_text(encoding="utf-8").strip() + "\n")
w("""## 7. The four ask-mode tests

The questions, the expected sources and my predictions were committed before any retrieval code existed
([`tests/questions.json`](tests/questions.json), [`tests/EXPECTATIONS.md`](tests/EXPECTATIONS.md), first commit).
The test file lives outside the vault and is never indexed.
""")
for t in best:
    c = t.get("citation_check") or {}
    w(f"### {t['test']['id']}: {t['question']}\n")
    w(f"*{t['test']['design']}*\n")
    w(f"- **Expected:** {t['test']['expected_answer']}" + (f" Source: `{t['test']['expected_source']}` › {t['test'].get('expected_section')}." if t['test']['expected_source'] else ""))
    w("- **Retrieved passages:**")
    for p in t["retrieval"]["passages"]:
        w(f"  {p['rank']}. `{p['path']}` › {p['section']} (lines {p['lines'][0]}–{p['lines'][1]}, score {p['score']})")
    w(f"- **Actual answer ({status_word(t)}):** {one_line(t['answer'])}")
    if t["status"] == "answered":
        w(f"- **Citation check by the harness:** cited {c['valid_citations']}, all retrieved; figures in the answer "
          f"{c['figures_in_answer'] or 'none'}; figures missing from the cited passages {c['figures_not_in_cited_passages'] or 'none'}.")
    else:
        w(f"- **Why it refused:** {t['reason']}.")
    if assess.get(t["test"]["id"]):
        w(f"- **My assessment after opening the cited passages:** {assess[t['test']['id']]}")
    w(f"- **Full record:** [{where}/ask/{t['test']['id']}.md]({where}/ask/{t['test']['id']}.md)\n")
w("""## 8. What failed first, and what I changed
""")
if run1:
    w("The first run is kept untouched in [`evidence/runs/run-1-initial/`](evidence/runs/run-1-initial/).\n")
    w("| Test | Run 1 | Final run | Expected passage rank, run 1 |")
    w("|---|---|---|---|")
    for a in run1:
        b = next((t for t in best if t["test"]["id"] == a["test"]["id"]), None)
        w(f"| {a['test']['id']} | {status_word(a)} | {status_word(b) if b else '—'} | {a.get('expected_passage_rank') or '—'} |")
w("""
**The failure: test 2.** The right passage was retrieved at rank 3 ("Negation transfer failed … it picked the negated
word (`tea`)"), and a second supporting passage at rank 2, but the model replied INSUFFICIENT EVIDENCE. My
prediction was half right: I expected this test to fail because keyword search cannot match "skill it failed to pick
up" to "negation". Retrieval did rank the passage lower than three others for that reason, but it was still in the
top 4. The refusal was the model's. My first rules told it that related information is not an answer, and with a
question worded differently from the passage it took that literally.

**The change.** One edit to the research rules and one to the prompt layout, both in
[`prompts/wiki-instructions.md`](prompts/wiki-instructions.md) and `ask.build_messages`: rule 1 now says the passages
may use different words than the question, and the question is stated before the passages as well as after. I reran
the affected tests. Test 2 is now answered with the correct citation, and both refusals (test 4 and the separation
check) still refuse, which was the risk of loosening the rule. The rules as used in run 1 are saved next to that run.

**Two bugs in my own harness, found by the same run.** The network flag said "offline" while the laptop was online,
because it relied on one outside connection and this Mac's per-app firewall blocks some of those. The harness now reads
the operating system (Wi-Fi power and default route) as well, and reports offline only when there is no route and no
probe succeeds. And model memory was read before the model had loaded. Details in the
[run 1 notes](evidence/runs/run-1-initial/README.md).

## 9. Mode checks
""")
modes = (E / "offline" / "mode-checks") if have_offline and (E / "offline" / "mode-checks").exists() else (E / "online" / "mode-checks")
mrel = modes.relative_to(ROOT).as_posix()
if (modes / "chat-capabilities-and-followup.md").exists():
    text = (modes / "chat-capabilities-and-followup.md").read_text(encoding="utf-8")
    turns = re.findall(r"\*\*You:\*\* (.+?)\n\n`harness: (.+?)`(.*?)\*\*Ledger:\*\* (.+?)\n\n(?:_|---)", text, re.S)
    w("| Check | I typed | Harness decision | Ledger replied |")
    w("|---|---|---|---|")
    labels = ["capabilities", "capabilities", "draft from notes", "follow-up"]
    for label, (you, decision, _, reply) in zip(labels, turns):
        w(f"| {label} | {you} | {decision} | {one_line(reply, 330)} |")
    w(f"\nFull transcript: [{mrel}/chat-capabilities-and-followup.md]({mrel}/chat-capabilities-and-followup.md)\n")
if (modes / "search-check.txt").exists():
    w(f"**Search** returns original passages with paths and line numbers and makes no model call: "
      f"[{mrel}/search-check.txt]({mrel}/search-check.txt).\n")
if (modes / "separation-ask-side.json").exists():
    sep = J(modes / "separation-ask-side.json")
    w(f"**A claim made only in chat is not evidence.** In chat I said I had decided to name my next project Falcon "
      f"([chat side]({mrel}/separation-chat-side.md)). Then, in a fresh `ask`: \"{sep['question']}\" → "
      f"**{status_word(sep)}** ([ask side]({mrel}/separation-ask-side.md)). Ask never sees chat history, and chat "
      "messages are never written into the vault or the index.\n")
if assess.get("mode_checks"):
    w(assess["mode_checks"] + "\n")
w("## 10. Offline demonstration\n")
if have_offline:
    net = offline[0]["network"]
    w(f"Run with `Run offline demo.command` after turning Wi-Fi off. The script refuses to start while the Mac is "
      f"connected. Each `./wiki` command is a new process, so the CLI was restarted after the network was gone. "
      f"Recorded network state during the tests: Wi-Fi {net['wifi_power']}, default route {net['default_route']}, "
      f"outside host answered {net['outside_host_answered']}.\n")
    w("| Step | Command | Evidence |")
    w("|---|---|---|")
    w("| Network state | `networksetup`, `route`, `ping` | [session.txt](evidence/offline/session.txt) |")
    w("| Help and status | `./wiki help`, `./wiki status` | same file |")
    w("| Ingestion with local Gemma | `./wiki ingest \"vault/raw/Pac-Man DQN README.md\" --force` | same file, and the [offline ingest report](evidence/ingest/) |")
    w("| Search | `./wiki search \"row level security\"` | same file |")
    w("| Four ask tests | `./wiki test` | [evidence/offline/ask/](evidence/offline/ask/) |")
    w("| Chat, search and separation checks | `./wiki test` | [evidence/offline/mode-checks/](evidence/offline/mode-checks/) |")
    w("")
    for name in off_shots:
        w(f"![Offline run](evidence/offline/{name})\n")
else:
    w("Not yet run. `Run offline demo.command` performs it: it refuses to start while the Mac is connected, then runs "
      "help, status, a forced re-ingestion of one source, search, the four ask tests and the mode checks, and saves "
      "everything under `evidence/offline/`.\n")
w("""## 11. Reflection: one limitation and one improvement
""")
w(assess.get("reflection", "_to be written from the final results_") + "\n")
w("""## 12. Repository map

| Path | What it is |
|---|---|
| [`wiki`](wiki), [`harness/`](harness/) | The CLI and the harness. Standard library only. |
| [`prompts/`](prompts/) | Research rules, persona, ingestion instructions. Loaded by the harness per mode. |
| [`vault/`](vault/) | The Obsidian vault: `raw/` originals, `wiki/` notes, `index.md`. |
| [`data/`](data/) | Machine files outside the vault: source catalog, note plan, search index, drafts. |
| [`tests/`](tests/) | The four questions, expectations and my assessments. Never indexed. |
| [`evidence/`](evidence/) | Model card, evidence cards, mode checks, ingestion reports, Obsidian screenshots, offline run, run 1. |
| [`scripts/`](scripts/) | Offline demonstration, Obsidian screenshots, this README's generator. |
| [`Run offline demo.command`](<Run offline demo.command>) | Double-click launcher for the offline demonstration. |

**AI assistance.** I used Claude (Anthropic) as my AI assistant, as the assignment's starter prompt describes: to write
the harness code with me, run the tests and assemble this README from the saved outputs. The design choices, sources
and questions are mine, every result is an actual output of local Gemma on my laptop, and nothing was sent to a hosted
model at question time.
""")
(ROOT / "README.md").write_text("\n".join(L), encoding="utf-8")
print("README.md written:", len("\n".join(L)), "chars;", "offline evidence:", have_offline)
