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

I trained a Deep Q-Network (DQN) on `ALE/MsPacman-v5` for a class assignment. My training involved specific hyperparameters and a learning process based on observations, actions, and rewards from the game.

## Key details

- I trained the DQN on `ALE/MsPacman-v5` with exploration set to 0.10, 500 training games, and a learning rate of 0.0001.
- Everything below comes from one executed run of `pacman_dqn.ipynb` on my Intel MacBook Pro (CPU).
- The notebook is saved with all cell outputs from that final run, and the evidence it produced is copied into `results/`.
- The mean score over the same 5 evaluation games was 492.0 for the untrained network and 608.0 for the trained agent.
- The change in mean score was +116.0.
- The agent's observations consist of four game screens shrunk to 84 × 84 grayscale pixels and stacked together.
- The agent's actions are joystick moves, with the network outputting nine numbers for no-op, up, right, left, down, and four diagonals.
- Rewards are game points, where rewards are clipped to between -1 and +1 for learning.

## Related notes

- (none yet)

## Sources

- [[Pac-Man DQN README#Ms. Pac-Man DQN — Class 3 assignment|Pac-Man DQN README § Ms. Pac-Man DQN — Class 3 assignment]] · source S3 · lines 3–17
- [[Pac-Man DQN README#5. What the agent sees, does, and is rewarded for (plain language)|Pac-Man DQN README § 5. What the agent sees, does, and is rewarded for (plain language)]] · source S3 · lines 202–216

Original file: `vault/raw/Pac-Man DQN README.md` (unchanged; SHA-256 `605a0ab0e419df4d…`)
