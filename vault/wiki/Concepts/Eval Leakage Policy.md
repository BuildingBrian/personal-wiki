---
title: Eval Leakage Policy
folder: Concepts
source_id: S1
source_file: raw/Custom LLM README.md
source_sha256: c8971e5d4ef04c14
source_sections:
  - "4. The fixed 48-case language evals"
  - "4. The fixed 48-case language evals > 4.4 How eval material stayed out of training"
generated_by: gemma4:e2b Q4_K_M (Ollama 0.20.7, local)
generated_at: 2026-09-29
reviewed: true
reviewed_by: Brian Arevalo Ramos, with Claude (AI assistant)
reviewed_at: 2026-09-29
---

# Eval Leakage Policy

I implemented a policy to prevent leakage of evaluation material into my training data. This involved specific procedures for handling evaluation sets and corpus content.

## Key details

- I withheld every classroom sentence containing a reserved test prefix before the split and vocabulary build (160 passages, method: `normalized contiguous prompt match; not a semantic leakage detector`).
- I avoided paired reference answers, ensuring the eval frame is never combined with an eval answer.
- I ensured chat transcripts and eval outputs were written only into the run folder, never into `corpus/`.
- I checked every imported passage with the same normalized substring test, and the process aborts on any hit.
- The eval correction pairs (red→blue, open→closed, tea→milk) never occur in my corpus, so the negation evals test transfer of the pattern to new nouns, not recall.
- `the opposite of hot is cold` never appears in the corpus. The same idea is taught in other frames, such as `hot is the opposite of cold`.
- Limit of the check: it is an exact contiguous match after normalisation, so it cannot detect paraphrases.

## Related notes

- [[Custom LLM Eval Results]] — Gives the scores this policy protects; they only count if no test material was trained on.
- [[Negation Failure]] — Shows the transfer test this policy made possible, and that the model failed it.

## Sources

- [[Custom LLM README#4. The fixed 48-case language evals|Custom LLM README § 4. The fixed 48-case language evals]] · source S1 · lines 311–317
- [[Custom LLM README#4.4 How eval material stayed out of training|Custom LLM README § 4.4 How eval material stayed out of training]] · source S1 · lines 428–438

Original file: `vault/raw/Custom LLM README.md` (unchanged; SHA-256 `c8971e5d4ef04c14…`)
