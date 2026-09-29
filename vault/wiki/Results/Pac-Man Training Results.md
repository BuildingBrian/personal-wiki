---
title: Pac-Man Training Results
folder: Results
source_id: S3
source_file: raw/Pac-Man DQN README.md
source_sha256: 605a0ab0e419df4d
source_sections:
  - "4. What actually happened > Training budget that was actually used"
  - "4. What actually happened > The five before-and-after scores"
  - "4. What actually happened > Training dashboard"
generated_by: gemma4:e2b Q4_K_M (Ollama 0.20.7, local)
generated_at: 2026-09-29
reviewed: true
reviewed_by: Brian Arevalo Ramos, with Claude (AI assistant)
reviewed_at: 2026-09-29
---

# Pac-Man Training Results

I completed all 500 requested training games in 79 minutes on CPU. The mean of the five fixed evaluation games rose from 492.0 to 608.0; four games improved and one (seed 404) got worse.

## Key details

- I completed training for 500 of 500 requested games.
- I recorded 296,988 agent decisions across 4 game frames each.
- I performed 73,998 learning updates in batches of 32.
- The elapsed training time, including every-25-game demos, was 1 h 19 min (79 min).
- I used an Intel Core i7-9750H (6 cores) with 32 GB RAM for the hardware.
- The untrained network baseline was used for the five before-and-after score comparisons.
- The mean score changed from 492.0 to 608.0, a change of +116.0.
- Seed by seed, untrained → trained: 350 → 530, 500 → 520, 320 → 680, 800 → 640, 490 → 670.

## Related notes

- [[Pac-Man Gameplay Progress]] — Shows gameplay scores fluctuate without a steady climb across training sessions.
- [[Pac-Man Training Choices]] — Gives the settings behind these results and what I expected before training.
- [[Custom LLM Eval Results]] — Gives the before-and-after scores of my language model, also measured on fixed tests.

## Sources

- [[Pac-Man DQN README#Training budget that was actually used|Pac-Man DQN README § Training budget that was actually used]] · source S3 · lines 106–121
- [[Pac-Man DQN README#The five before-and-after scores|Pac-Man DQN README § The five before-and-after scores]] · source S3 · lines 125–138
- [[Pac-Man DQN README#Training dashboard|Pac-Man DQN README § Training dashboard]] · source S3 · lines 144–154

Original file: `vault/raw/Pac-Man DQN README.md` (unchanged; SHA-256 `605a0ab0e419df4d…`)
