---
title: Experiment Next Steps
folder: Lessons
source_id: S3
source_file: raw/Pac-Man DQN README.md
source_sha256: 605a0ab0e419df4d
source_sections:
  - "7. Next experiment (change exactly one setting)"
generated_by: gemma4:e2b Q4_K_M (Ollama 0.20.7, local)
generated_at: 2026-09-29
reviewed: false
---

# Experiment Next Steps

The next experiment involves changing exactly one setting to test the effect of replay capacity. The goal is to observe how a larger memory affects agent behavior and learning.

## Key details

- Change one setting: replay capacity 5,000 → 50,000.
- Keep exploration 0.10, 500 episodes, and learning rate 0.0001 exactly as they were.
- A ten-times-larger memory (about 1.7 GB of pixels) would let each batch of 32 mix experiences from roughly 80 games instead of 8.
- This is the mechanism the DQN paper relies on to stabilize learning.
- The 25-game average should keep rising past the 912 ceiling instead of oscillating around 700.
- The seed-101 checkpoint scores should stop swinging by a factor of five.
- Trained games should finally get *longer* than untrained ones.

## Related notes

- [[PacMan DQN Project]] — This note describes the next step in the experiment to test replay capacity.
- [[Agent Learning Limitations]] — This note describes the limitations observed in the previous agent learning process.
- [[Training Results Analysis]] — This note details the results obtained from the training process.

## Sources

- [[Pac-Man DQN README#7. Next experiment (change exactly one setting)|Pac-Man DQN README § 7. Next experiment (change exactly one setting)]] · source S3 · lines 235–244

Original file: `vault/raw/Pac-Man DQN README.md` (unchanged; SHA-256 `605a0ab0e419df4d…`)
