---
title: Custom LLM Project
folder: Projects
source_id: S1
source_file: raw/Custom LLM README.md
source_sha256: c8971e5d4ef04c14
source_sections:
  - "Building a Custom LLM with nanoGPT — MBA 290T Class 4 (Assignment 3)"
  - "2. My runs"
generated_by: gemma4:e2b Q4_K_M (Ollama 0.20.7, local)
generated_at: 2026-09-29
reviewed: true
reviewed_by: Brian Arevalo Ramos, with Claude (AI assistant)
reviewed_at: 2026-09-29
---

# Custom LLM Project

I trained Andrej Karpathy's nanoGPT twice on my Intel MacBook's CPU for an assignment. Both runs used the same settings, seed, split rule, and evaluation panels.

## Key details

- I trained nanoGPT with 2 blocks, 4 heads, 64-number embeddings, 48-token context, and whole-word tokens.
- I ran the training once on the supplied classroom corpus and again after adding my own synthetic teaching files for three extension skills.
- Both runs used the same settings, seed, split rule, and evaluation panels.
- Experiment 1 took 22.2 s to complete training, while Experiment 2 took 38.9 s.
- Both experiments used the same hardware: Intel Core i7-9750H (6 cores), CPU only, macOS 26.6, Python 3.12.14, and PyTorch 2.2.2.
- The split is by deduplicated passage, meaning a validation passage can share its template with training passages.
- The held-out loss measures whether the model learned templates rather than memorizing specific sentences.

## Related notes

- [[Custom LLM Training Choices]] — Gives the three choices I made before training, corpus, steps and learning rate, and the prediction I wrote down.
- [[Custom LLM Training Evidence]] — Gives detailed evidence of the loss curves, weight updates, and next-token probabilities from the training process.
- [[Custom LLM Eval Results]] — Gives the scores on the fixed 48-case evals, before and after training, for both experiments.
- [[Pac-Man DQN Project]] — Describes the other model I trained on this laptop's CPU, a game-playing agent rather than a language model.

## Sources

- [[Custom LLM README#Building a Custom LLM with nanoGPT — MBA 290T Class 4 (Assignment 3)|Custom LLM README § Building a Custom LLM with nanoGPT — MBA 290T Class 4 (Assignment 3)]] · source S1 · lines 3–10
- [[Custom LLM README#2. My runs|Custom LLM README § 2. My runs]] · source S1 · lines 97–116

Original file: `vault/raw/Custom LLM README.md` (unchanged; SHA-256 `c8971e5d4ef04c14…`)
