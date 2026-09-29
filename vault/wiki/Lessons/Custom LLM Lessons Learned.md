---
title: Custom LLM Lessons Learned
folder: Lessons
source_id: S1
source_file: raw/Custom LLM README.md
source_sha256: c8971e5d4ef04c14
source_sections:
  - "6. What I learned"
generated_by: gemma4:e2b Q4_K_M (Ollama 0.20.7, local)
generated_at: 2026-09-29
reviewed: true
reviewed_by: Brian Arevalo Ramos, with Claude (AI assistant)
reviewed_at: 2026-09-29
---

# Custom LLM Lessons Learned

I learned about the components and processes involved in training my custom LLM. I discovered how the model learned from my data, the role of attention, and the limitations of what the model actually understands.

## Key details

- My corpus consists of 6,559 short passages: 4,592 template sentences about eight everyday domains plus my 1,967 teaching sentences.
- The corpus can teach which words go together in which slots. It cannot teach grammar it never shows, facts it never states, or long-range reasoning.
- A token is a piece of text the tokenizer cut out, and its ID is an arbitrary integer label, such as 28 in one run or 81 in the other.
- The vector is the row of 64 floating-point numbers stored at that ID in the embedding table, and "embedding" is the name for that learned mapping from ID to vector.
- The loss is the negative log probability the model gave the true next word, averaged over a batch.
- Backpropagation computes how much the loss would change if a weight moved, and AdamW moves each weight against its gradient by a step scaled by the learning rate.
- I performed 3,000 repetitions, which took the loss from 4.93 to 0.68.
- Attention builds a weighted average of the vectors at earlier positions, with weights the model learned to compute from the tokens.

## Related notes

- [[Tokens And Embeddings]] — Describes the process of converting text into numerical representations used by the model.
- [[Negation Failure]] — Shows how the model's understanding has limitations when dealing with negation in text.
- [[Next Steps And Hardware]] — Lists what I plan to try next, from the negation experiment to training models on images.

## Sources

- [[Custom LLM README#6. What I learned|Custom LLM README § 6. What I learned]] · source S1 · lines 490–515

Original file: `vault/raw/Custom LLM README.md` (unchanged; SHA-256 `c8971e5d4ef04c14…`)
