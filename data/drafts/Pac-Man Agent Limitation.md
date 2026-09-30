---
title: Pac-Man Agent Limitation
folder: Lessons
source_id: S3
source_file: raw/Pac-Man DQN README.md
source_sha256: 605a0ab0e419df4d
source_sections:
  - "6. One limitation I observed"
  - "7. Next experiment (change exactly one setting)"
generated_by: gemma4:e2b Q4_K_M (Ollama 0.20.7, local)
generated_at: 2026-09-29
reviewed: false
---

# Pac-Man Agent Limitation

I observed that the agent did not learn to avoid ghosts, and 500 games with a 5,000-decision memory were insufficient for learning. This limitation stems from design choices in the classroom DQN.

## Key details

- The agent did not learn to avoid ghosts.
- 500 games with a 5,000-decision memory were not enough to expect learning.
- The replay memory holds about eight games, so every update is drawn from the agent's most recent behavior and older lessons are overwritten.
- Losing a life carries no negative reward, so a death only shows up indirectly as future points that never arrive.
- A smaller caveat is that five evaluation games is a small sample.
- One of the five evaluation games (seed 404) got worse (800 → 640).
- The +116 mean improvement is real for this run but should not be read as a precise measure of the agent's skill.

## Related notes

- (none yet)

## Sources

- [[Pac-Man DQN README#6. One limitation I observed|Pac-Man DQN README § 6. One limitation I observed]] · source S3 · lines 222–231
- [[Pac-Man DQN README#7. Next experiment (change exactly one setting)|Pac-Man DQN README § 7. Next experiment (change exactly one setting)]] · source S3 · lines 235–244

Original file: `vault/raw/Pac-Man DQN README.md` (unchanged; SHA-256 `605a0ab0e419df4d…`)
