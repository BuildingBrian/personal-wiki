"""The retrieval tool: a local BM25 keyword index over passages of the ORIGINAL sources."""
import json
import math
import re
import time
from collections import Counter

from . import chunking, config
from .textutil import terms

K1, B = 1.5, 0.75


class IndexMissing(RuntimeError):
    pass


def build(catalog):
    """Rebuild the whole index from vault/raw. Cheap: no model involved."""
    records, df = [], Counter()
    for entry in catalog["sources"]:
        path = config.VAULT / entry["path"]
        text = path.read_text(encoding="utf-8", errors="replace")
        for n, passage in enumerate(chunking.passages(text), 1):
            tf = Counter(terms(passage["text"]))
            for term in terms(passage["section"]):       # heading words count twice
                tf[term] += 2
            if not tf:
                continue
            records.append({"id": f"{entry['id']}-P{n:03d}", "source_id": entry["id"], "source": entry["name"],
                            "path": "vault/" + entry["path"], "section": passage["section"],
                            "lines": [passage["start"], passage["end"]], "text": passage["text"],
                            "tf": dict(tf), "length": sum(tf.values())})
            df.update(tf.keys())
    index = {"built_at": time.strftime("%Y-%m-%dT%H:%M:%S"), "method": "BM25 (k1=1.5, b=0.75), stdlib only",
             "passage_words": config.PASSAGE_WORDS, "sources": {e["id"]: e["sha256"] for e in catalog["sources"]},
             "average_length": sum(r["length"] for r in records) / max(len(records), 1),
             "document_frequency": dict(df), "passages": records}
    config.PASSAGES.parent.mkdir(parents=True, exist_ok=True)
    config.PASSAGES.write_text(json.dumps(index, ensure_ascii=False), encoding="utf-8")
    return index


def load():
    if not config.PASSAGES.exists():
        raise IndexMissing("No search index yet. Run:  ./wiki ingest vault/raw")
    return json.loads(config.PASSAGES.read_text(encoding="utf-8"))


def search(query, k=config.TOP_K, index=None):
    """Return the k best passages with scores, plus how much of the query they cover."""
    index = index or load()
    wanted = list(dict.fromkeys(terms(query)))
    total, avg, df = len(index["passages"]), index["average_length"], index["document_frequency"]
    known = [t for t in wanted if t in df]
    scored = []
    for passage in index["passages"]:
        score, matched = 0.0, []
        for term in known:
            freq = passage["tf"].get(term, 0)
            if not freq:
                continue
            idf = math.log(1 + (total - df[term] + 0.5) / (df[term] + 0.5))
            score += idf * freq * (K1 + 1) / (freq + K1 * (1 - B + B * passage["length"] / avg))
            matched.append(term)
        if score > 0:
            scored.append((score, matched, passage))
    scored.sort(key=lambda item: -item[0])
    hits = []
    for rank, (score, matched, passage) in enumerate(scored[:k], 1):
        hits.append({"rank": rank, "score": round(score, 2), "matched_terms": matched,
                     "coverage": round(len(matched) / max(len(wanted), 1), 2),
                     **{key: passage[key] for key in ("id", "source_id", "source", "path", "section", "lines", "text")}})
    return {"query": query, "query_terms": wanted, "terms_not_in_index": [t for t in wanted if t not in df], "hits": hits}


def notes():
    """The reviewed wiki notes as routing entries: title, source id, and the source sections each note was written
    from (its `source_sections` property). Read from vault/wiki on every call, so a renamed note is picked up."""
    entries = []
    for path in sorted(config.WIKI.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---"):
            continue
        _, front, body = text.split("---", 2)
        source = re.search(r"^source_id:\s*(\S+)", front, re.M)
        if not source:
            continue
        tf = Counter(terms(body.split("## Sources")[0]))
        for term in terms(path.stem):                   # title words count twice, like headings in passages
            tf[term] += 2
        entries.append({"title": path.stem, "source_id": source.group(1),
                        "sections": re.findall(r'^\s+-\s+"(.*)"\s*$', front, re.M),
                        "tf": tf, "length": sum(tf.values())})
    return entries


def route(query):
    """Score the wiki notes against the query with the same BM25 formula. Returns [(score, note)], best first."""
    entries = notes()
    if not entries:
        return []
    df = Counter(term for note in entries for term in note["tf"])
    total, avg = len(entries), sum(n["length"] for n in entries) / len(entries)
    scored = []
    for note in entries:
        score = 0.0
        for term in dict.fromkeys(terms(query)):
            freq = note["tf"].get(term, 0)
            if freq:
                idf = math.log(1 + (total - df[term] + 0.5) / (df[term] + 0.5))
                score += idf * freq * (K1 + 1) / (freq + K1 * (1 - B + B * note["length"] / avg))
        if score > 0:
            scored.append((round(score, 2), note))
    return sorted(scored, key=lambda item: -item[0])


def retrieve(query, k=config.TOP_K, index=None):
    """The retrieval used by ask and search. Keyword search alone misses a section that explains something in
    different words (test 3: "stop another user reading" versus "RLS policies"). So the harness also asks which
    reviewed wiki note matches best, and brings in up to ROUTED_MAX passages from that note's source sections,
    replacing the weakest keyword hits. No model is involved."""
    index = index or load()
    everything = search(query, len(index["passages"]), index)
    ranked = everything["hits"]
    notes_ranked = route(query)
    extra, note = [], None
    if notes_ranked:
        note = notes_ranked[0][1]

        def from_note(hit):
            return hit["source_id"] == note["source_id"] and any(
                hit["section"] == s or hit["section"].endswith("> " + s) for s in note["sections"])

        keyword_ids = {h["id"] for h in ranked[:k]}
        extra = [h for h in ranked if from_note(h) and len(h["matched_terms"]) >= config.ROUTED_MIN_TERMS]
        extra = [h for h in extra[:config.ROUTED_MAX] if h["id"] not in keyword_ids]
    hits = [dict(h, via="keyword") for h in ranked[:k - len(extra)]]
    hits += [dict(h, via=f"wiki note: {note['title']}", keyword_rank=h["rank"]) for h in extra]
    for rank, hit in enumerate(hits, 1):
        hit["rank"] = rank
    everything.update(hits=hits, routed_note=note["title"] if note else None,
                      note_scores=[[score, n["title"]] for score, n in notes_ranked[:3]])
    return everything
