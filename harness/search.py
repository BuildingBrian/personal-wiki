"""Search mode: show the original passages. Never calls the model."""
from . import config, index


def run(query, k=config.TOP_K + 1, out=None):
    import sys
    out = out or sys.stdout
    result = index.search(query, k)
    print(f'SEARCH  "{query}"   (keyword index over original sources; no model call, no generated answer)', file=out)
    print(f"query terms: {', '.join(result['query_terms']) or '(none)'}"
          + (f"   not in any source: {', '.join(result['terms_not_in_index'])}" if result["terms_not_in_index"] else ""), file=out)
    if not result["hits"]:
        print("\nNo passage matches these words.", file=out)
        return result
    for hit in result["hits"]:
        print(f"\n[{hit['rank']}] {hit['path']}  ›  {hit['section']}  (lines {hit['lines'][0]}–{hit['lines'][1]})", file=out)
        print(f"    passage {hit['id']} · score {hit['score']} · matched: {', '.join(hit['matched_terms'])}", file=out)
        for line in hit["text"].splitlines():
            print("    | " + line, file=out)
    return result
