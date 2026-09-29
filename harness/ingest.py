"""Ingest mode: register sources, rebuild the search index, and have local Gemma draft linked wiki notes.

The model writes summaries, details and link reasons. The harness decides file names, folders, source references and
properties, so no machine-style name can reach the vault, and ingesting the same source twice changes nothing.
"""
import hashlib
import json
import math
import re
import sys
import time
from collections import Counter

from . import chunking, config, index, model
from .textutil import numbers, terms, word_count

SKIP = re.compile(r"table of contents|^screenshots?$|licen[sc]e|acknowledg|evidence index|^sources$|repository layout", re.I)
INTRO = ("This wiki is my memory of the projects I built in MBA 290T: what I built, what I measured, what failed, and "
         "what I said I would try next. Notes are drafted by a local Gemma model from my own write-ups and reviewed "
         "by me against the originals. Every note links back to the passage it came from.")
FOLDER_BLURB = {"Projects": "What each project is and how it was built.",
                "Results": "What was measured, with the numbers.",
                "Concepts": "Ideas and mechanisms the projects rely on.",
                "Lessons": "What failed, what I learned, and what I would try next."}


def _load(path, default):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def _save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def register():
    """Give every file in vault/raw a stable id and record its hash. Originals are only ever read."""
    catalog = _load(config.CATALOG, {"sources": []})
    origins = _load(config.DATA / "source_origins.json", {})
    known = {e["path"]: e for e in catalog["sources"]}
    changes = {}
    files = sorted(p for p in config.RAW.rglob("*") if p.is_file() and not p.name.startswith(".")
                   and p.suffix.lower() in (".md", ".markdown", ".txt"))
    for path in files:
        rel = path.relative_to(config.VAULT).as_posix()
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        entry = known.get(rel)
        if entry is None:
            entry = {"id": f"S{len(catalog['sources']) + 1}", "name": path.stem, "path": rel, "sha256": digest,
                     "added": time.strftime("%Y-%m-%d")}
            catalog["sources"].append(entry)
            changes[rel] = "new"
        elif entry["sha256"] != digest:
            entry.update(sha256=digest, updated=time.strftime("%Y-%m-%d"))
            changes[rel] = "changed"
        else:
            changes[rel] = "unchanged"
        entry["words"] = word_count(path.read_text(encoding="utf-8", errors="replace"))
        entry.update(origins.get(rel, {}))
    _save(config.CATALOG, catalog)
    return catalog, changes


def units(text):
    """Planning units: top-level sections, with very long sections split at their sub-headings."""
    grouped, order = {}, []
    for block in chunking.blocks(text):
        grouped.setdefault(block["top_section"], []).append(block)
        if block["top_section"] not in order:
            order.append(block["top_section"])
    out = []
    for top in order:
        group = grouped[top]
        parts = {}
        for block in group:
            sub = " > ".join(block["section"].split(" > ")[:2])
            parts.setdefault(sub, []).append(block)
        chosen = parts if sum(word_count(b["text"]) for b in group) > 600 and len(parts) > 1 else {top: group}
        for heading, blocks in chosen.items():
            anchor = heading.split(" > ")[-1]
            body = "\n\n".join(b["text"] for b in blocks)
            if SKIP.search(anchor) or word_count(body) < 25:
                continue
            out.append({"heading": heading, "anchor": anchor, "text": body, "words": word_count(body),
                        "lines": [blocks[0]["start"], blocks[-1]["end"]]})
    for n, unit in enumerate(out, 1):
        unit["n"] = n
    return out


def clean_title(raw):
    title = re.sub(r"[\\/:*?\"<>|#^\[\]`*_]", " ", raw)
    title = re.sub(r"^\s*[\d.]+\s*", "", title)
    title = re.sub(r"\s+", " ", title).strip(" .-")
    return " ".join(w if w.isupper() or "-" in w else w[:1].upper() + w[1:] for w in title.split())


def parse_plan(reply, all_units, taken, project):
    notes, valid = [], {u["n"] for u in all_units}
    for line in reply.splitlines():
        match = re.match(r"\s*[-*]?\s*NOTE\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*([\d,\s]+)", line, re.I)
        if not match:
            continue
        title = clean_title(match.group(1))
        folder = next((f for f in config.FOLDERS if f.lower().startswith(match.group(2).strip().lower()[:5])), "Projects")
        picked = [n for n in dict.fromkeys(int(x) for x in re.findall(r"\d+", match.group(3))) if n in valid]
        if not (2 <= len(title.split()) <= 6) or not picked:
            continue
        if title.lower() in taken:
            title = f"{title} - {project}"
        taken.add(title.lower())
        notes.append({"title": title, "folder": folder, "units": picked})
    return notes


def fallback_plan(all_units, taken, project):
    """Used only if the model's plan cannot be parsed: the four longest sections, titled from their headings."""
    notes = []
    for unit in sorted(all_units, key=lambda u: -u["words"])[:4]:
        title = clean_title(unit["anchor"])
        title = " ".join(title.split()[:4])
        if project.split()[0].lower() not in title.lower():
            title = f"{project} {title}"
        if title.lower() in taken:
            continue
        taken.add(title.lower())
        notes.append({"title": title, "folder": "Projects", "units": [unit["n"]]})
    return notes


def make_plan(entry, all_units, taken, out):
    project = re.sub(r"\s*README$", "", entry["name"], flags=re.I)
    listing = "\n".join(f"{u['n']}. {u['heading']} ({u['words']} words): \"{' '.join(u['text'].split()[:16])}\""
                        for u in all_units)
    prompt = (f"You are organising a personal wiki. Below are the numbered sections of one document about the project "
              f"\"{project}\".\n"
              "Group the sections into 4 to 6 wiki notes. Each note covers ONE subject. Leave out sections about "
              "setup, installation or file listings.\n"
              "Title rules: 2 to 5 natural words in Title Case that a person would search for. Put the project name "
              f"\"{project}\" in the title when the subject belongs to this project. No punctuation, no numbers at the start.\n"
              f"Folders: Projects (what it is, how it was built), Results (what was measured), Concepts (ideas and "
              "mechanisms), Lessons (failures, limitations, next steps).\n"
              "Reply with one line per note, exactly in this form and nothing else:\n"
              "NOTE | <title> | <folder> | <section numbers separated by commas>\n\n"
              f"Sections:\n{listing}")
    reply, stats = model.chat([{"role": "user", "content": prompt}], max_tokens=260, temperature=0.2, purpose="ingest-plan")
    notes = parse_plan(reply, all_units, taken, project)
    source = "model"
    if len(notes) < 2:
        notes, source = fallback_plan(all_units, taken, project), "fallback (model plan could not be parsed)"
    print(f"    plan from {source}: {len(notes)} notes in {stats['wall_seconds']} s", file=out)
    return {"planned_by": source, "planned_at": time.strftime("%Y-%m-%d"), "notes": notes}


def condense(text, budget):
    """Fit a section into a word budget: long tables and code blocks are shortened before prose is cut."""
    kept, used = [], 0
    for block in text.split("\n\n"):
        lines = block.split("\n")
        if lines[0].lstrip().startswith("|") and len(lines) > 8:
            block = "\n".join(lines[:8] + [f"| ... {len(lines) - 8} more rows not shown |"])
        elif lines[0].lstrip().startswith("```") and len(lines) > 10:
            block = "\n".join(lines[:9] + ["...", "```"])
        size = word_count(block)
        if used + size > budget:
            if not kept:
                kept.append(" ".join(block.split()[:budget]))
            break
        kept.append(block)
        used += size
    return "\n\n".join(kept)


def parse_note(reply):
    summary = re.search(r"SUMMARY:\s*(.+?)(?=\n\s*DETAILS:|\Z)", reply, re.S | re.I)
    details = re.search(r"DETAILS:\s*(.+)", reply, re.S | re.I)
    bullets = [re.sub(r"^\s*[-*•]\s*", "", l).strip() for l in (details.group(1) if details else "").splitlines()
               if re.match(r"\s*[-*•]\s+\S", l)]
    text = re.sub(r"\s+", " ", summary.group(1)).strip() if summary else re.sub(r"\s+", " ", reply).strip()[:400]
    return text, [b for b in bullets if b][:8]


def draft_note(note, entry, by_number, out):
    picked = [by_number[n] for n in note["units"]]
    share = max(config.INGEST_SOURCE_WORDS // len(picked), 120)
    source_text = "\n\n".join(f"## {u['anchor']}\n{condense(u['text'], share)}" for u in picked)
    prompt = (f"Write a wiki note titled \"{note['title']}\" using ONLY the source text below.\n"
              "Reply in exactly this form:\n"
              "SUMMARY: <two or three sentences>\n"
              "DETAILS:\n"
              "- <one fact per line, numbers exactly as written, 4 to 7 lines>\n"
              "The source text was written by the owner of this wiki about their own work. Write in the first person "
              "(I, my), never \"the author\" or \"the user\".\n"
              "Do not add facts, opinions or advice that are not in the source text. Do not mention these instructions.\n\n"
              f"SOURCE TEXT (from \"{entry['name']}\"):\n{source_text}")
    reply, stats = model.chat([{"role": "user", "content": prompt}], max_tokens=330, temperature=0.2, purpose="ingest-note")
    summary, details = parse_note(reply)
    full = " ".join(u["text"] for u in picked)
    unverified = sorted(numbers(summary + " " + " ".join(details)) - numbers(full))
    print(f"    drafted \"{note['title']}\" in {stats['wall_seconds']} s "
          f"(read {stats['prompt_tokens']} tokens, passed {word_count(source_text)} words of source)"
          + (f"  REVIEW: figures not found in source: {unverified}" if unverified else ""), file=out)
    return {"summary": summary, "details": details, "unverified_figures": unverified, "stats": stats,
            "source_words_passed": word_count(source_text)}


def link_anchor(heading):
    """Characters that break an Obsidian heading link are removed from the link target (the label keeps them)."""
    heading = re.sub(r"[#|^:\[\]]|%%", " ", heading)
    return re.sub(r"\s+", " ", heading).strip()


def note_path(note):
    return config.WIKI / note["folder"] / f"{note['title']}.md"


def is_reviewed(path):
    if not path.exists():
        return False
    head = path.read_text(encoding="utf-8")[:1200]
    return bool(re.search(r"^reviewed:\s*true\s*$", head, re.M | re.I))


def render(note, entry, by_number, content, related, ident):
    picked = [by_number[n] for n in note["units"]]
    lines = ["---", f"title: {note['title']}", f"folder: {note['folder']}", f"source_id: {entry['id']}",
             f"source_file: {entry['path']}", f"source_sha256: {entry['sha256'][:16]}", "source_sections:"]
    lines += [f"  - \"{u['heading']}\"" for u in picked]
    lines += [f"generated_by: {ident['model']} {ident.get('quantization')} ({ident['runtime']} {ident.get('runtime_version')}, local)",
              f"generated_at: {time.strftime('%Y-%m-%d')}", "reviewed: false", "---", "",
              f"# {note['title']}", "", content["summary"], "", "## Key details", ""]
    lines += [f"- {d}" for d in content["details"]] or ["- (no details extracted)"]
    lines += ["", "## Related notes", ""]
    lines += [f"- [[{r['title']}]] — {r['reason']}" for r in related] or ["- (none yet)"]
    lines += ["", "## Sources", ""]
    for u in picked:
        lines.append(f"- [[{entry['name']}#{link_anchor(u['anchor'])}|{entry['name']} § {u['anchor']}]] "
                     f"· source {entry['id']} · lines {u['lines'][0]}–{u['lines'][1]}")
    lines += ["", f"Original file: `vault/{entry['path']}` (unchanged; SHA-256 `{entry['sha256'][:16]}…`)", ""]
    return "\n".join(lines)


def similar(a, b):
    shared = set(a) & set(b)
    top = sum(a[t] * b[t] for t in shared)
    return top / (math.sqrt(sum(v * v for v in a.values())) * math.sqrt(sum(v * v for v in b.values())) or 1)


def link_reasons(title, summary, candidates, out):
    listing = "\n".join(f"{n}. \"{c['title']}\": {c['summary']}" for n, c in enumerate(candidates, 1))
    prompt = (f"Current wiki note \"{title}\": {summary}\n\nCandidate related notes:\n{listing}\n\n"
              "For each candidate that is genuinely connected to the current note, write one line in this form:\n"
              "<number> | <one short sentence saying how it connects>\n"
              "Skip candidates that are not connected. Write nothing else.")
    reply, stats = model.chat([{"role": "user", "content": prompt}], max_tokens=150, temperature=0.2, purpose="ingest-links")
    related = []
    for line in reply.splitlines():
        match = re.match(r"\s*(\d+)\s*\|\s*(.+)", line)
        if match and 1 <= int(match.group(1)) <= len(candidates):
            reason = match.group(2).strip().rstrip(".") + "."
            related.append({"title": candidates[int(match.group(1)) - 1]["title"], "reason": reason})
    print(f"    linked \"{title}\" to {len(related)} notes in {stats['wall_seconds']} s", file=out)
    return related


def read_note(path):
    text = path.read_text(encoding="utf-8")
    body = text.split("---", 2)[2] if text.startswith("---") else text
    match = re.search(r"^# .+?\n+(.+?)(?=\n## |\Z)", body.strip(), re.S | re.M)
    summary = re.sub(r"\s+", " ", match.group(1)).strip() if match else ""
    return {"title": path.stem, "folder": path.parent.name, "summary": summary, "text": body}


def write_index(catalog, out):
    notes = sorted((read_note(p) for p in config.WIKI.rglob("*.md")), key=lambda n: n["title"])
    lines = ["# Project Wiki", "", INTRO, "",
             f"{len(notes)} notes from {len(catalog['sources'])} sources. Start with a topic below, open a note, then "
             "follow its **Sources** link to the original passage.", ""]
    for folder in config.FOLDERS:
        group = [n for n in notes if n["folder"] == folder]
        if not group:
            continue
        lines += [f"## {folder}", "", FOLDER_BLURB[folder], ""]
        for n in group:
            first = re.split(r"(?<=[.!?])\s", n["summary"])[0] if n["summary"] else ""
            lines.append(f"- [[{n['title']}]] — {first}")
        lines.append("")
    lines += ["## Source catalog", "", "Originals live unchanged in `raw/`. The id is what evidence files and note "
              "properties refer to.", "", "| ID | Source | Original file | Origin | Words | SHA-256 | Added |",
              "|---|---|---|---|---|---|---|"]
    for e in catalog["sources"]:
        lines.append(f"| {e['id']} | [[{e['name']}]] | `{e.get('original_filename', e['path'])}` | "
                     f"{e.get('origin', 'local file')} | {e.get('words', '')} | `{e['sha256'][:12]}…` | {e['added']} |")
    lines.append("")
    config.INDEX_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"  index.md rebuilt: {len(notes)} notes, {len(catalog['sources'])} sources", file=out)
    return notes


def retire_unplanned(plan, out):
    """After a rename or merge in the plan, the old generated file would be a duplicate. Move it out of the vault.
    A note a human has reviewed is never moved; it is reported instead."""
    planned = {note_path(n).resolve() for p in plan.values() for n in p["notes"]}
    retired = []
    for path in sorted(config.WIKI.rglob("*.md")):
        if path.resolve() in planned:
            continue
        if is_reviewed(path):
            print(f"  WARNING: reviewed note not in the plan, left in place: {path.relative_to(config.VAULT)}", file=out)
            continue
        target = config.DRAFTS / "retired" / path.name
        target.parent.mkdir(parents=True, exist_ok=True)
        path.replace(target)
        retired.append(path.relative_to(config.VAULT).as_posix())
        print(f"  retired {path.relative_to(config.VAULT)} (no longer in the plan; kept in data/drafts/retired/)", file=out)
    for folder in sorted(config.WIKI.glob("*")):
        if folder.is_dir() and not any(folder.iterdir()):
            folder.rmdir()
    return retired


def run(targets=None, force=False, replan=False, out=None):
    out = out or sys.stdout
    started = time.time()
    before = {p.relative_to(config.VAULT).as_posix() for p in config.WIKI.rglob("*.md")} if config.WIKI.exists() else set()
    catalog, changes = register()
    print(f"INGEST  {len(catalog['sources'])} sources in vault/raw", file=out)
    for entry in catalog["sources"]:
        print(f"  {entry['id']}  {entry['path']}  ({entry['words']} words)  {changes.get(entry['path'], 'missing')}", file=out)
    built = index.build(catalog)
    print(f"  search index rebuilt: {len(built['passages'])} passages (no model needed for this step)", file=out)

    wanted = None
    if targets:
        wanted = set()
        for target in targets:
            resolved = (config.ROOT / target).resolve() if not str(target).startswith("/") else __import__("pathlib").Path(target)
            for entry in catalog["sources"]:
                source = (config.VAULT / entry["path"]).resolve()
                if source == resolved or resolved in source.parents:
                    wanted.add(entry["id"])
        if not wanted:
            print(f"  no source matches {targets}. Sources must be inside vault/raw.", file=out)
            return {"error": "no matching source"}

    plan = _load(config.PLAN, {})
    ident = model.identity()
    taken = {n["title"].lower() for p in plan.values() for n in p["notes"]}
    report = {"created": [], "updated": [], "kept_reviewed": [], "up_to_date": [], "flags": {}, "drafts": []}
    touched = []
    for entry in catalog["sources"]:
        if wanted is not None and entry["id"] not in wanted:
            continue
        text = (config.VAULT / entry["path"]).read_text(encoding="utf-8", errors="replace")
        all_units = units(text)
        by_number = {u["n"]: u for u in all_units}
        if entry["id"] not in plan or replan:
            print(f"  planning notes for {entry['id']} {entry['name']} ({len(all_units)} sections)", file=out)
            if entry["id"] in plan:
                taken -= {n["title"].lower() for n in plan[entry["id"]]["notes"]}
            plan[entry["id"]] = make_plan(entry, all_units, taken, out)
            _save(config.PLAN, plan)
        notes = plan[entry["id"]]["notes"]
        stale = changes.get(entry["path"]) in ("new", "changed") or force
        print(f"  {entry['id']} {entry['name']}: {len(notes)} notes planned", file=out)
        for note in notes:
            note["units"] = [n for n in note["units"] if n in by_number]
            path = note_path(note)
            if path.exists() and not stale:
                report["up_to_date"].append(note["title"])
                continue
            content = draft_note(note, entry, by_number, out)
            report["drafts"].append({"note": note["title"], "source": entry["id"],
                                     "source_words_passed": content["source_words_passed"], **content["stats"]})
            if content["unverified_figures"]:
                report["flags"][note["title"]] = content["unverified_figures"]
            page = render(note, entry, by_number, content, [], ident)
            if is_reviewed(path):
                config.DRAFTS.mkdir(parents=True, exist_ok=True)
                (config.DRAFTS / f"{note['title']}.md").write_text(page, encoding="utf-8")
                report["kept_reviewed"].append(note["title"])
                print(f"    kept the reviewed note; the fresh draft is in data/drafts/ for comparison", file=out)
                continue
            (report["updated"] if path.exists() else report["created"]).append(note["title"])
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(page, encoding="utf-8")
            touched.append((note, entry, by_number, content))

    if touched:
        everything = [read_note(p) for p in config.WIKI.rglob("*.md")]
        vectors = {n["title"]: Counter(terms(n["title"] + " " + n["text"])) for n in everything}
        print(f"  linking {len(touched)} notes", file=out)
        for note, entry, by_number, content in touched:
            ranked = sorted((n for n in everything if n["title"] != note["title"]),
                            key=lambda n: -similar(vectors[note["title"]], vectors[n["title"]]))
            candidates = [n for n in ranked if similar(vectors[note["title"]], vectors[n["title"]]) > 0.08][:4]
            related = link_reasons(note["title"], content["summary"], candidates, out)[:3] if candidates else []
            note_path(note).write_text(render(note, entry, by_number, content, related, ident), encoding="utf-8")

    report["retired"] = retire_unplanned(plan, out)
    write_index(catalog, out)
    after = {p.relative_to(config.VAULT).as_posix() for p in config.WIKI.rglob("*.md")}
    planned = {note_path(n).relative_to(config.VAULT).as_posix() for p in plan.values() for n in p["notes"]}
    report.update(notes_before=len(before), notes_after=len(after), new_files=sorted(after - before),
                  unplanned_files=sorted(after - planned), seconds=round(time.time() - started, 1))
    print(f"\n  created {len(report['created'])} · updated {len(report['updated'])} · kept reviewed "
          f"{len(report['kept_reviewed'])} · already up to date {len(report['up_to_date'])}", file=out)
    print(f"  notes in vault/wiki: {report['notes_before']} before, {report['notes_after']} after · "
          f"files outside the plan (duplicates): {len(report['unplanned_files'])}", file=out)
    if report["flags"]:
        print("  figures to check by hand against the source:", file=out)
        for title, figures in report["flags"].items():
            print(f"    {title}: {figures}", file=out)
    print(f"  done in {report['seconds']} s", file=out)
    from . import evidence
    report.update(command="ingest " + " ".join(str(t) for t in (targets or ["vault/raw"])) + (" --force" if force else ""),
                  **evidence.stamp())
    folder = config.EVIDENCE / "ingest"
    folder.mkdir(parents=True, exist_ok=True)
    name = time.strftime("ingest-%Y%m%d-%H%M%S") + ("-offline" if not report["internet_reachable"] else "")
    (folder / f"{name}.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"  report saved to evidence/ingest/{name}.json", file=out)
    return report
