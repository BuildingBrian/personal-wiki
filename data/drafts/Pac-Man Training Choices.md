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

I made three specific choices for my Pac-Man training: Exploration, Episodes, and Learning rate. I chose these values based on the constraints of the notebook and the limited replay memory.

## Key details

- For Exploration, I chose a value of 0.10, which is 10 % of training moves being random.
- For Episodes, I chose 500, which is five times the starting value of 100.
- For the Learning rate, I chose 0.0001.
- I chose 500 episodes because the notebook warned that useful Atari learning "may require much longer runs".
- I chose a smaller learning rate because with a tiny replay memory, larger steps risk divergence.
- I expected an untrained baseline around 300–800 points per game.
- I expected modest, noisy improvement rather than mastery, expecting the trained mean to land around 600–900.
- I expected a jagged training curve and a loss that does not simply go down.

## Related notes

- (none yet)

## Sources

- [[Pac-Man DQN README#2. My three choices and why|Pac-Man DQN README § 2. My three choices and why]] · source S3 · lines 67–79
- [[Pac-Man DQN README#3. What I expected before training|Pac-Man DQN README § 3. What I expected before training]] · source S3 · lines 85–98

Original file: `vault/raw/Pac-Man DQN README.md` (unchanged; SHA-256 `605a0ab0e419df4d…`)
