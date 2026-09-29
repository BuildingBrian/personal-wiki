---
title: Pac-Man Training Choices
folder: Projects
source_id: S3
source_file: raw/Pac-Man DQN README.md
source_sha256: 605a0ab0e419df4d
source_sections:
  - "2. My three choices and why"
  - "3. What I expected before training"
generated_by: gemma4:e2b Q4_K_M (Ollama 0.20.7, local)
generated_at: 2026-09-29
reviewed: true
reviewed_by: Brian Arevalo Ramos, with Claude (AI assistant)
reviewed_at: 2026-09-29
---

# Pac-Man Training Choices

I made three specific choices for my Pac-Man training: Exploration, Episodes, and Learning rate. I chose these values based on the limitations of my replay memory and the need to fit the training within a deadline.

## Key details

- For Exploration, I chose a value of 0.10, which is 10% of training moves being random.
- For Episodes, I chose 500, which is five times the starting value of 100.
- For the Learning rate, I chose 0.0001, which is the reference point for Adam in DQN implementations.
- I wanted most of my replay memory to be the agent's own policy rather than coin flips due to the limited memory.
- I expected the untrained baseline to be around 300–800 points per game.
- I expected modest, noisy improvement rather than mastery, as 500 games is roughly 1–2% of the experience the original DQN paper used.
- I expected a jagged training curve and a loss that does not simply go down.

## Related notes

- [[Pac-Man Training Results]] — Gives what these choices produced: a mean score of 608.0 against 492.0 untrained.
- [[Pac-Man Agent Limitation]] — Shows why the chosen training parameters were insufficient for learning to avoid ghosts.
- [[Custom LLM Training Choices]] — Gives the choices and the prediction I wrote before training my language model, including a learning rate of 0.001.

## Sources

- [[Pac-Man DQN README#2. My three choices and why|Pac-Man DQN README § 2. My three choices and why]] · source S3 · lines 67–79
- [[Pac-Man DQN README#3. What I expected before training|Pac-Man DQN README § 3. What I expected before training]] · source S3 · lines 85–98

Original file: `vault/raw/Pac-Man DQN README.md` (unchanged; SHA-256 `605a0ab0e419df4d…`)
