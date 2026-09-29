"""Check the vault the way a reader would: names, headings, links, source references. No model involved."""
import json
import re
import sys

from . import config

LINK = re.compile(r"\[\[([^\]|#]+)(?:#([^\]|]+))?(?:\|([^\]]+))?\]\]")
MACHINE = re.compile(r"([0-9a-f]{8,}|\d{8,}|\d{4}-\d{2}-\d{2}|--|__|task[-_ ]?\d|chunk[-_ ]?\d)", re.I)
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$", re.M)


def anchor(text):
    """Heading text as Obsidian compares it in a link: formatting and link-breaking characters removed."""
    text = re.sub(r"[*_`]", "", text)
    text = re.sub(r"[#|^:\[\]]|%%", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def run(out=None):
    out = out or sys.stdout
    files = {}
    for path in config.VAULT.rglob("*.md"):
        if ".obsidian" in path.parts or ".trash" in path.parts:
            continue
        files.setdefault(path.stem.lower(), []).append(path)
    notes = sorted(config.WIKI.rglob("*.md"))
    problems, links_checked, source_refs = [], 0, 0
    plan = json.loads(config.PLAN.read_text(encoding="utf-8")) if config.PLAN.exists() else {}
    planned = {n["title"] for p in plan.values() for n in p["notes"]}

    for note in notes:
        rel = note.relative_to(config.VAULT).as_posix()
        text = note.read_text(encoding="utf-8")
        words = note.stem.split()
        if not 2 <= len(words) <= 6:
            problems.append(f"{rel}: file name has {len(words)} words (want 2 to 6)")
        if MACHINE.search(note.stem):
            problems.append(f"{rel}: file name looks machine-made")
        first = HEADING.search(text.split("---", 2)[2] if text.startswith("---") else text)
        if not first or first.group(2).strip() != note.stem:
            problems.append(f"{rel}: first heading does not match the file name")
        if len(files[note.stem.lower()]) > 1:
            problems.append(f"{rel}: another file has the same name, links to it are ambiguous")
        if note.stem not in planned:
            problems.append(f"{rel}: not in the note plan (possible duplicate)")
        if "## Sources" not in text or "[[" not in text.split("## Sources")[-1]:
            problems.append(f"{rel}: no source reference")

    for path in notes + ([config.INDEX_MD] if config.INDEX_MD.exists() else []):
        rel = path.relative_to(config.VAULT).as_posix()
        for target, heading, _label in LINK.findall(path.read_text(encoding="utf-8")):
            links_checked += 1
            found = files.get(target.strip().split("/")[-1].lower(), [])
            if not found:
                problems.append(f"{rel}: link to missing note [[{target}]]")
                continue
            if len(found) > 1:
                problems.append(f"{rel}: link [[{target}]] is ambiguous ({len(found)} files)")
            if heading:
                source_refs += 1
                headings = {anchor(h) for _, h in HEADING.findall(found[0].read_text(encoding="utf-8"))}
                if anchor(heading) not in headings:
                    problems.append(f"{rel}: [[{target}#{heading}]] points to a heading that does not exist")

    for title in sorted(planned):
        if title.lower() not in files:
            problems.append(f"planned note missing from the vault: {title}")

    print(f"CHECK  {len(notes)} wiki notes · {links_checked} links · {source_refs} source references", file=out)
    print(f"  file names 2 to 6 words, no machine-style names, first heading = file name, every note in the plan,", file=out)
    print(f"  every link resolves to exactly one file, every source reference points to a real heading", file=out)
    if problems:
        print(f"\n  {len(problems)} problems:", file=out)
        for p in problems:
            print("   - " + p, file=out)
    else:
        print("\n  0 problems", file=out)
    return problems
