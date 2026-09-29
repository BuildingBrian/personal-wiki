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
reviewed: true
reviewed_by: Brian Arevalo Ramos, with Claude (AI assistant)
reviewed_at: 2026-09-29
---

# Custom LLM Chat Interface

I use the instructor's terminal loop, `chat.py`, as my chat interface to interact with my tiny language model. This model continues a prompt rather than answering it, lacks conversation memory, and reports unknown words.

## Key details

- The interface is the instructor's terminal loop `chat.py`.
- It loads my Experiment 2 weights and vocabulary from `model.pt`.
- The model continues a prompt instead of answering it, starting each prompt with a fresh context.
- Unknown words are reported and mapped to `<UNK>`.
- Only the last 48 tokens of a long prompt are used.
- Generating replies never updates weights or touches the corpus.
- I launch it using the command: `.venv/bin/python chat.py --model evidence/expanded/model.pt --transcript my_chat.json`.

## Related notes

- [[Custom LLM Project]] — Describes the model behind the chat: nanoGPT with a 48-token context and whole-word tokens.
- [[Sampling Temperature]] — Explains what the temperature setting does when the chat samples each next word.

## Sources

- [[Custom LLM README#5. Chat interface|Custom LLM README § 5. Chat interface]] · source S1 · lines 451–486

Original file: `vault/raw/Custom LLM README.md` (unchanged; SHA-256 `c8971e5d4ef04c14…`)
