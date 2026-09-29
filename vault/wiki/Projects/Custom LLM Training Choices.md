---
title: Custom LLM Training Choices
folder: Projects
source_id: S1
source_file: raw/Custom LLM README.md
source_sha256: c8971e5d4ef04c14
source_sections:
  - "1. My choices and prediction"
generated_by: gemma4:e2b Q4_K_M (Ollama 0.20.7, local)
generated_at: 2026-09-29
reviewed: true
reviewed_by: Brian Arevalo Ramos, with Claude (AI assistant)
reviewed_at: 2026-09-29
---

# Custom LLM Training Choices

I made three choices before training: the corpus, 3,000 training steps and a learning rate of 0.001. I kept steps and learning rate identical in both experiments so the corpus was the only variable, and I wrote my prediction in the notebook before training.

## Key details

- Experiment 1 used only the supplied classroom sentences as the corpus.
- Experiment 2 added 1,967 new unique passages that I generated with `tools/make_teaching_data.py`.
- The corpus included files for opposites (699 lines), categories and analogies (648 lines), and negation (620 lines).
- I used 3,000 training steps in both runs, with one step being a batch of 32 passages.
- I used a learning rate of 0.001, with a warmup and cosine decay.
- The corpus was the only variable between the two experiments.
- My prediction, written before training: opposites and categories would become scorable and beat chance (above 25%). Outcome: 3/3 each.
- My prediction for negation: scorable but near chance, because it requires copying a word, which is harder than association. Outcome: 1/3, which is chance.

## Related notes

- [[Custom LLM Eval Results]] — Gives the measured outcome of these choices: 20 of 48 correct on the starter corpus and 30 of 48 on the expanded one.
- [[Custom LLM Project]] — Describes the model and the two runs these choices were made for.
- [[Pac-Man Training Choices]] — Gives the three choices and the prediction I wrote before training my Pac-Man agent, including a learning rate of 0.0001.

## Sources

- [[Custom LLM README#1. My choices and prediction|Custom LLM README § 1. My choices and prediction]] · source S1 · lines 44–93

Original file: `vault/raw/Custom LLM README.md` (unchanged; SHA-256 `c8971e5d4ef04c14…`)
