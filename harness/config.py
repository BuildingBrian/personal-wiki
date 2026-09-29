"""Every path and setting the harness uses, in one place."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / "vault"              # open THIS folder in Obsidian
RAW = VAULT / "raw"                 # original sources, never modified
WIKI = VAULT / "wiki"               # generated and reviewed notes
INDEX_MD = VAULT / "index.md"       # human landing page
DATA = ROOT / "data"                # machine files live outside the vault
CATALOG = DATA / "catalog.json"     # source ids, original names, hashes
PLAN = DATA / "plan.json"           # which sections feed which note (keeps re-ingestion stable)
PASSAGES = DATA / "index" / "passages.json"
DRAFTS = DATA / "drafts"            # fresh model drafts of notes a human has already reviewed
LOGS = DATA / "logs"
PROMPTS = ROOT / "prompts"
EVIDENCE = ROOT / "evidence"
OUTPUTS = ROOT / "outputs"          # chat drafts saved with /save, kept apart from evidence

MODEL = os.environ.get("WIKI_MODEL", "gemma4:e2b")
OLLAMA_URL = os.environ.get("WIKI_OLLAMA_URL", "http://127.0.0.1:11434")
NUM_CTX = 4096                      # one context size everywhere, so the model is never reloaded
KEEP_ALIVE = "30m"

PASSAGE_WORDS = 130                 # target passage size
PASSAGE_MAX_WORDS = 190
TOP_K = 4                           # passages sent to the model in ask mode
CHAT_TOP_K = 3
CHAT_SUBJECT_ALIASES = ["language model", "nanogpt", "llm", "dqn", "tracker", "row level security"]
CHAT_HISTORY_TURNS = 6              # user+assistant messages kept as conversation context
INGEST_SOURCE_WORDS = 900           # most source text passed to the model for one note
FOLDERS = ["Projects", "Results", "Concepts", "Lessons"]
