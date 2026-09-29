---
title: PacMan DQN Project
folder: Concepts
source_id: S3
source_file: raw/Pac-Man DQN README.md
source_sha256: 605a0ab0e419df4d
source_sections:
  - "2. My three choices and why"
  - "4. What actually happened > Training budget that was actually used"
  - "4. What actually happened > The five before-and-after scores"
  - "4. What actually happened > Training dashboard"
  - "6. One limitation I observed"
  - "7. Next experiment (change exactly one setting)"
generated_by: gemma4:e2b Q4_K_M (Ollama 0.20.7, local)
generated_at: 2026-09-29
reviewed: false
---

# PacMan DQN Project

The PacMan DQN project involved training an agent using specific settings and observed limitations regarding learning ghosts and memory. The agent's performance improved significantly after training, but the learning process showed plateaus and oscillations.

## Key details

- The exploration setting was set to 0.10, with a default value of 0.20.
- The training involved 500 episodes and 100 evaluation episodes.
- The training budget used 500 completed training games.
- The agent made 296,988 agent decisions across 4 game frames each.
- The elapsed training time was 1 hour 19 minutes (79 minutes).
- The hardware used was an Intel Core i7-9750H with 6 cores and 32 GB RAM.
- The mean score increased from 492.0 in the untrained network to 608.0 after training.

## Related notes

- [[Training Results Analysis]] — This note describes the overall context of the PacMan DQN project.
- [[Initial Expectations]] — This note details the quantitative results of the training process.
- [[Agent Learning Limitations]] — This note describes the initial goals and predictions for the learning process.

## Sources

- [[Pac-Man DQN README#2. My three choices and why|Pac-Man DQN README § 2. My three choices and why]] · source S3 · lines 67–79
- [[Pac-Man DQN README#Training budget that was actually used|Pac-Man DQN README § Training budget that was actually used]] · source S3 · lines 106–121
- [[Pac-Man DQN README#The five before-and-after scores|Pac-Man DQN README § The five before-and-after scores]] · source S3 · lines 125–138
- [[Pac-Man DQN README#Training dashboard|Pac-Man DQN README § Training dashboard]] · source S3 · lines 144–154
- [[Pac-Man DQN README#6. One limitation I observed|Pac-Man DQN README § 6. One limitation I observed]] · source S3 · lines 222–231
- [[Pac-Man DQN README#7. Next experiment (change exactly one setting)|Pac-Man DQN README § 7. Next experiment (change exactly one setting)]] · source S3 · lines 235–244

Original file: `vault/raw/Pac-Man DQN README.md` (unchanged; SHA-256 `605a0ab0e419df4d…`)
