---
title: LLM Concepts And Mechanisms
folder: Concepts
source_id: S1
source_file: raw/Custom LLM README.md
source_sha256: c8971e5d4ef04c14
source_sections:
  - "1. My choices and prediction"
generated_by: gemma4:e2b Q4_K_M (Ollama 0.20.7, local)
generated_at: 2026-09-29
reviewed: false
---

# LLM Concepts And Mechanisms

The text describes two experiments involving different corpora to train a model, focusing on word associations, categories, and negation. The results showed that the model learned associations in the second experiment but struggled with negation, aligning with predictions.

## Key details

- Experiment 1 used only the supplied classroom sentences as the corpus.
- Experiment 2 added 1,967 new unique passages to the corpus.
- The vocabulary increased from 133 to 385 word types, remaining under the 509-type cap.
- The training steps for both runs were 3,000.
- The learning rate was set to 0.001, with a warmup and cosine decay applied.
- The corpus was the only variable between the two experiments.
- In Experiment 1, opposites and categories became scorable and beat chance (above 25%) in Experiment 2.
- Negation scored 1/3 in Experiment 2, which is near chance.

## Related notes

- [[Custom LLM Lessons Learned]] — This note describes the results of experiments involving training a model on different corpora.
- [[Custom LLM Language Evals]] — This note details the evaluation process used for the Custom LLM.
- [[Custom LLM Evidence From Network]] — This note provides specific measurements and observations from a Custom LLM experiment.

## Sources

- [[Custom LLM README#1. My choices and prediction|Custom LLM README § 1. My choices and prediction]] · source S1 · lines 44–93

Original file: `vault/raw/Custom LLM README.md` (unchanged; SHA-256 `c8971e5d4ef04c14…`)
