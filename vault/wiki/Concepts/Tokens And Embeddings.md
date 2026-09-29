---
title: Tokens And Embeddings
folder: Concepts
source_id: S1
source_file: raw/Custom LLM README.md
source_sha256: c8971e5d4ef04c14
source_sections:
  - "3. Evidence from inside the network > 3.3 One word, from text to ID to 64-number vector"
  - "3. Evidence from inside the network > 3.6 Attention rows"
generated_by: gemma4:e2b Q4_K_M (Ollama 0.20.7, local)
generated_at: 2026-09-29
reviewed: true
reviewed_by: Brian Arevalo Ramos, with Claude (AI assistant)
reviewed_at: 2026-09-29
---

# Tokens And Embeddings

I use a process to convert one word from text into an ID and then into a 64-number vector. This process involves tokenization, vocabulary mapping, and an embedding table.

## Key details

- The tokenizer lower-cases the text and splits it into words and punctuation using a regular expression.
- The vocabulary is built only from training passages and maps each word type to an integer ID.
- `<BOS>` is ID 1 and `<EOS>` is ID 2.
- An ID is just a label, and the numbering can change based on the vocabulary size in different experiments.
- The embedding table is a 136 × 64 matrix of weights.
- The vector for the word `customer` is found in row 28 of the embedding table.
- The vector for `customer` starts as random numbers (-0.0576, -0.0048, 0.0426, …) and after 3,000 steps reads 0.0366, -0.0182, 0.1330, …. The full 64 numbers are in the source.

## Related notes

- [[Custom LLM Training Evidence]] — Gives the loss curves and the first real weight update on the `customer` vector traced here.
- [[Custom LLM Lessons Learned]] — Explains in plain words how a token, its ID, its vector and an embedding differ.
- [[Sampling Temperature]] — Explains how the scores computed from these vectors become a sampled word.

## Sources

- [[Custom LLM README#3.3 One word, from text to ID to 64-number vector|Custom LLM README § 3.3 One word, from text to ID to 64-number vector]] · source S1 · lines 194–235
- [[Custom LLM README#3.6 Attention rows|Custom LLM README § 3.6 Attention rows]] · source S1 · lines 265–274

Original file: `vault/raw/Custom LLM README.md` (unchanged; SHA-256 `c8971e5d4ef04c14…`)
