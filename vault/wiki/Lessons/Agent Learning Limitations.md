---
title: Agent Learning Limitations
folder: Lessons
source_id: S3
source_file: raw/Pac-Man DQN README.md
source_sha256: 605a0ab0e419df4d
source_sections:
  - "6. One limitation I observed"
generated_by: gemma4:e2b Q4_K_M (Ollama 0.20.7, local)
generated_at: 2026-09-29
reviewed: false
---

# Agent Learning Limitations

The agent failed to learn to avoid ghosts, and the training process showed unstable results. This was partly due to design choices in the classroom DQN.

## Key details

- The agent did not learn to avoid ghosts.
- 500 games with a 5,000-decision memory were not enough to expect learning.
- Trained games were no longer than untrained games (571 vs 589 decisions).
- The seed-101 checkpoint score swung between 190 and 1,100 with no trend.
- The 25-game average plateaued after roughly game 25.
- The replay memory holds about eight games, so every update is drawn from the agent's most recent behavior and older lessons are overwritten.
- Losing a life carries no negative reward.
- A death only shows up indirectly as future points that never arrive.

## Related notes

- [[PacMan DQN Project]] — This note describes the specific failure to learn ghost avoidance and unstable results in the context of the PacMan DQN project.
- [[Training Results Analysis]] — This note details the quantitative results of the training process, including the score increase and the timing of learning.
- [[Initial Expectations]] — This note outlines the author's initial predictions about the learning process, which contrasts with the actual unstable results.

## Sources

- [[Pac-Man DQN README#6. One limitation I observed|Pac-Man DQN README § 6. One limitation I observed]] · source S3 · lines 222–231

Original file: `vault/raw/Pac-Man DQN README.md` (unchanged; SHA-256 `605a0ab0e419df4d…`)
