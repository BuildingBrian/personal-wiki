"""Split a Markdown or text source into passages that keep their source path, section and line numbers."""
import re

from . import config
from .textutil import word_count

HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
NOISE = re.compile(r"^\s*(!\[[^\]]*\]\([^)]*\)|-{3,}|\*{3,}|</?details>|<summary>.*</summary>|</?[a-z]+/?>)\s*$", re.I)


def _clean_heading(text):
    return re.sub(r"[*_`]", "", text).strip()


def blocks(text):
    """Yield paragraphs, tables and code blocks with their section path and line range."""
    out, stack, current, start, in_code = [], [], [], None, False

    def flush(end):
        nonlocal current, start
        body = [line for line in current if not NOISE.match(line)]
        if any(line.strip() for line in body):
            titles = [t for level, t in stack if level > 1] or [t for _, t in stack]
            out.append({"text": "\n".join(body).strip("\n"), "start": start, "end": end,
                        "section": " > ".join(titles) if titles else "(top)",
                        "top_section": titles[0] if titles else "(top)"})
        current, start = [], None

    for number, line in enumerate(text.split("\n"), 1):
        if line.strip().startswith("```"):
            if not in_code:
                flush(number - 1)
                in_code, current, start = True, [line], number
            else:
                current.append(line)
                in_code = False
                flush(number)
            continue
        if in_code:
            current.append(line)
            continue
        match = HEADING.match(line)
        if match:
            flush(number - 1)
            level = len(match.group(1))
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, _clean_heading(match.group(2))))
            continue
        if not line.strip():
            flush(number - 1)
            continue
        if start is None:
            start = number
        current.append(line)
    flush(len(text.split("\n")))
    return out


def _split_large(block):
    """A block longer than the maximum is cut: tables by rows (header repeated), prose by sentences."""
    text, limit = block["text"], config.PASSAGE_WORDS
    lines = text.split("\n")
    if lines[0].lstrip().startswith("|"):
        header = lines[:2] if len(lines) > 1 and set(lines[1]) <= set("|-: ") else lines[:1]
        pieces, rows = [], []
        for row in lines[len(header):]:
            rows.append(row)
            if word_count("\n".join(rows)) >= limit:
                pieces.append("\n".join(header + rows))
                rows = []
        if rows:
            pieces.append("\n".join(header + rows))
        return pieces
    if lines[0].lstrip().startswith("```"):
        pieces, rows = [], []
        for row in lines[1:-1]:
            rows.append(row)
            if word_count("\n".join(rows)) >= limit:
                pieces.append("```\n" + "\n".join(rows) + "\n```")
                rows = []
        if rows:
            pieces.append("```\n" + "\n".join(rows) + "\n```")
        return pieces
    pieces, sentences = [], []
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        sentences.append(sentence)
        if word_count(" ".join(sentences)) >= limit:
            pieces.append(" ".join(sentences))
            sentences = []
    if sentences:
        pieces.append(" ".join(sentences))
    return pieces


def passages(text):
    """Group consecutive blocks of one section into passages of about PASSAGE_WORDS words."""
    out, pending = [], []

    def flush():
        nonlocal pending
        if pending:
            out.append({"text": "\n\n".join(b["text"] for b in pending), "section": pending[0]["section"],
                        "top_section": pending[0]["top_section"], "start": pending[0]["start"], "end": pending[-1]["end"]})
        pending = []

    for block in blocks(text):
        if pending and block["section"] != pending[0]["section"]:
            flush()
        if word_count(block["text"]) > config.PASSAGE_MAX_WORDS:
            flush()
            for piece in _split_large(block):
                out.append({"text": piece, "section": block["section"], "top_section": block["top_section"],
                            "start": block["start"], "end": block["end"]})
            continue
        pending.append(block)
        if sum(word_count(b["text"]) for b in pending) >= config.PASSAGE_WORDS:
            flush()
    flush()
    return out


def sections(text):
    """Top-level sections of a source (used by ingestion to plan notes)."""
    grouped, order = {}, []
    for block in blocks(text):
        key = block["top_section"]
        if key not in grouped:
            grouped[key] = {"heading": key, "text": [], "start": block["start"], "end": block["end"]}
            order.append(key)
        grouped[key]["text"].append(block["text"])
        grouped[key]["end"] = block["end"]
    return [{**grouped[k], "text": "\n\n".join(grouped[k]["text"])} for k in order]
