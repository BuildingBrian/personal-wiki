---
title: Custom LLM Chat Interface
folder: Projects
source_id: S1
source_file: raw/Custom LLM README.md
source_sha256: c8971e5d4ef04c14
source_sections:
  - "5. Chat interface"
generated_by: gemma4:e2b Q4_K_M (Ollama 0.20.7, local)
generated_at: 2026-09-29
reviewed: false
---

# Custom LLM Chat Interface

The chat interface uses the instructor's terminal loop `chat.py` to load weights and vocabulary from `model.pt`. It functions by continuing a prompt rather than answering it, without conversation memory.

## Key details

- The interface uses the instructor's terminal loop `chat.py` to load Experiment 2 weights and vocabulary from `model.pt`.
- It is a tiny language model that continues a prompt instead of answering it, starting each prompt with a fresh context.
- Unknown words are reported and mapped to `<UNK>`.
- Only the last 48 tokens of a long prompt are used.
- Generating replies never updates weights or touches the corpus.
- The launch command is `.venv/bin/python chat.py --model evidence/expanded/model.pt --transcript my_chat.json`.
- The model identity is `llm_runs/20260922T044308_125561Z` with model sha256 `5593b08e1e84afcc7a136b720178e4af76c4e360032c587074677d9d3066a2a3`.
- The transcript file is `evidence/expanded/chat_transcript_terminal.json` with temperature 0.8, max 24 tokens, and seeds 2026+turn.

## Related notes

- [[Custom LLM Evidence From Network]] — This document details measurements and observations from the Custom LLM.

## Sources

- [[Custom LLM README#5. Chat interface|Custom LLM README § 5. Chat interface]] · source S1 · lines 451–486

Original file: `vault/raw/Custom LLM README.md` (unchanged; SHA-256 `c8971e5d4ef04c14…`)
