---
title: Initial Expectations
folder: Results
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

# Initial Expectations

The initial expectations were based on a 5-episode setup check and predictions about the learning process. The author expected a modest, noisy improvement rather than mastery, and anticipated a jagged training curve.

## Key details

- The untrained baseline was expected to be around 300–800 points per game.
- The agent was expected to learn that continuing along an unfinished pellet row pays and that some moves near ghosts end the game.
- Deliberate ghost avoidance, power-pellet hunting, or clearing a maze were not expected because 500 games is roughly 1–2 % of the experience the original DQN paper used.
- A jagged training curve with a 25-game average that drifts up slowly and can fall back was expected.
- A loss that does not simply go down was expected, as the network's value estimates grow and the targets move with them.
- There was a real chance of no improvement or regression on the five fixed evaluation games due to constant 10 % exploration with a 5,000-decision memory.

## Related notes

- [[Training Results Analysis]] — This note describes the initial expectations set before the actual training results were analyzed.
- [[PacMan DQN Project]] — This note details the specific training process and initial results that informed the expectations.
- [[Agent Learning Limitations]] — This note describes the limitations encountered during the learning process, which relates to the expected noisy improvement.

## Sources

- [[Pac-Man DQN README#2. My three choices and why|Pac-Man DQN README § 2. My three choices and why]] · source S3 · lines 67–79
- [[Pac-Man DQN README#3. What I expected before training|Pac-Man DQN README § 3. What I expected before training]] · source S3 · lines 85–98

Original file: `vault/raw/Pac-Man DQN README.md` (unchanged; SHA-256 `605a0ab0e419df4d…`)
