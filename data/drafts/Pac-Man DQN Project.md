---
title: Pac-Man DQN Project
folder: Projects
source_id: S3
source_file: raw/Pac-Man DQN README.md
source_sha256: 605a0ab0e419df4d
source_sections:
  - "Ms. Pac-Man DQN — Class 3 assignment"
  - "5. What the agent sees, does, and is rewarded for (plain language)"
generated_by: gemma4:e2b Q4_K_M (Ollama 0.20.7, local)
generated_at: 2026-09-29
reviewed: false
---

# Pac-Man DQN Project

I trained a Deep Q-Network (DQN) on `ALE/MsPacman-v5` for a class assignment. I used specific parameters and learned how the agent perceives the game environment and learns from rewards.

## Key details

- I trained the DQN on `ALE/MsPacman-v5` with exploration set to 0.10, 500 training games, and a learning rate of 0.0001.
- The results from one executed run of `pacman_dqn.ipynb` on my Intel MacBook Pro (CPU) are copied into `results/`.
- The mean score for the trained agent was 608.0, compared to 492.0 for the untrained network.
- The change in mean score was +116.0 across the five individual scores.
- The agent observes four game screens shrunk to 84 × 84 grayscale pixels and stacked together.
- The agent's actions are joystick moves, with the network outputting nine numbers for the nine joystick positions.
- Rewards are game points, where rewards are clipped to between -1 and +1 for learning.
- The agent learns by storing its last 5,000 decisions and replaying 32 random ones every four decisions.

## Related notes

- (none yet)

## Sources

- [[Pac-Man DQN README#Ms. Pac-Man DQN — Class 3 assignment|Pac-Man DQN README § Ms. Pac-Man DQN — Class 3 assignment]] · source S3 · lines 3–17
- [[Pac-Man DQN README#5. What the agent sees, does, and is rewarded for (plain language)|Pac-Man DQN README § 5. What the agent sees, does, and is rewarded for (plain language)]] · source S3 · lines 202–216

Original file: `vault/raw/Pac-Man DQN README.md` (unchanged; SHA-256 `605a0ab0e419df4d…`)
