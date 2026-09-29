---
title: Custom LLM Training Evidence
folder: Results
source_id: S1
source_file: raw/Custom LLM README.md
source_sha256: c8971e5d4ef04c14
source_sections:
  - "3. Evidence from inside the network > 3.1 Loss curves"
  - "3. Evidence from inside the network > 3.4 One real gradient and weight update"
  - "3. Evidence from inside the network > 3.5 Next-token probabilities before and after (prefix the customer)"
generated_by: gemma4:e2b Q4_K_M (Ollama 0.20.7, local)
generated_at: 2026-09-29
reviewed: true
reviewed_by: Brian Arevalo Ramos, with Claude (AI assistant)
reviewed_at: 2026-09-29
---

# Custom LLM Training Evidence

I have documented evidence regarding my custom LLM training, focusing on loss curves, weight updates, and next-token probabilities. These records detail the process of training, including initial states and subsequent updates.

## Key details

- I fixed panels of 20 training and 20 validation documents for loss curve measurements.
- I averaged the cross-entropy over non-padding next-token targets.
- The notebook records the panels at step 0, halfway, and the end, resulting in three points per curve.
- Experiment 1 loss at step 0 was 4.9263 for training and 4.9275 for validation.
- Experiment 2 loss at step 0 was 5.9482 for training and 5.9767 for validation.
- The first weight update for `customer`'s embedding row at step 0 involved a gradient of 0.000693.
- In Experiment 2, the first update for `customer` was -0.032742, moving to -0.032732 with a gradient of -0.002369.
- For the prefix `the customer`, the top untrained word in Experiment 1 was `customer` at 0.0160. After training the top word was `reviewed` at 0.1782 in Experiment 1 and `recommended` at 0.1770 in Experiment 2.

## Related notes

- [[Custom LLM Project]] — Shows the specific parameters and context used during the custom LLM training process.
- [[Custom LLM Training Choices]] — Shows the specific corpus and parameters used for the training documented in the evidence.
- [[Tokens And Embeddings]] — Traces the word `customer` from text to ID to the 64-number vector whose first weight this evidence follows.

## Sources

- [[Custom LLM README#3.1 Loss curves|Custom LLM README § 3.1 Loss curves]] · source S1 · lines 122–139
- [[Custom LLM README#3.4 One real gradient and weight update|Custom LLM README § 3.4 One real gradient and weight update]] · source S1 · lines 239–249
- [[Custom LLM README#3.5 Next-token probabilities before and after (prefix the customer)|Custom LLM README § 3.5 Next-token probabilities before and after (prefix the customer)]] · source S1 · lines 253–261

Original file: `vault/raw/Custom LLM README.md` (unchanged; SHA-256 `c8971e5d4ef04c14…`)
