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
reviewed: false
---

# Pac-Man Training Choices

I made three specific choices for my Pac-Man training parameters. I chose an exploration rate of 0.10, 500 episodes, and a learning rate of 0.0001. These choices were based on my assessment of the limited replay memory and the need to ensure the training fit within a deadline.

## Key details

- For Exploration, I chose a value of 0.10, while the notebook default was 0.20.
- I set the number of Episodes to 500, compared to the default of 100.
- I selected a Learning rate of 0.0001, which is the reference point for Adam in DQN implementations.
- I wanted most of the replay memory to be the agent's own policy rather than coin flips due to the limited memory.
- I expected the untrained baseline to be around 300–800 points per game.
- I anticipated modest, noisy improvement rather than mastery, expecting the trained mean to be around 600–900.
- I expected a jagged training curve and a loss that does not simply go down.
- I anticipated a real chance of no improvement or regression on the five fixed evaluation games.

## Related notes

- (none yet)

## Sources

- [[Pac-Man DQN README#2. My three choices and why|Pac-Man DQN README § 2. My three choices and why]] · source S3 · lines 67–79
- [[Pac-Man DQN README#3. What I expected before training|Pac-Man DQN README § 3. What I expected before training]] · source S3 · lines 85–98

Original file: `vault/raw/Pac-Man DQN README.md` (unchanged; SHA-256 `605a0ab0e419df4d…`)
