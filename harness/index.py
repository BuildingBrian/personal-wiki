"""The retrieval tool: a local BM25 keyword index over passages of the ORIGINAL sources."""
import json
import math
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
