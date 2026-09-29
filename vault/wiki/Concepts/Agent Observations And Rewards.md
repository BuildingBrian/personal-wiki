---
title: Agent Observations And Rewards
folder: Concepts
source_id: S3
source_file: raw/Pac-Man DQN README.md
source_sha256: 605a0ab0e419df4d
source_sections:
  - "5. What the agent sees, does, and is rewarded for (plain language)"
generated_by: gemma4:e2b Q4_K_M (Ollama 0.20.7, local)
generated_at: 2026-09-29
reviewed: false
---

# Agent Observations And Rewards

The agent observes four game screens, takes joystick moves, and is rewarded based on changes in game score. The agent learns by storing decisions and updating its guesses based on received rewards and the best guess for the next screen.

## Key details

- Observations consist of four game screens shrunk to 84 × 84 grayscale pixels and stacked together.
- One screen shows where everything is, and four in a row show which way everything is moving.
- Actions are joystick moves, with nine outputs for no-op, up, right, left, down, and the four diagonals.
- The agent most of the time takes the highest guess for the number of future points that move leads to.
- Rewards are the change in score after each decision, such as 10 for a pellet or 200+ for a ghost.
- For learning, each reward is clipped to between -1 and +1 so a ghost is not much louder than a pellet.
- The agent stores its last 5,000 decisions and replays 32 random ones every four decisions.
- The agent nudges its guesses toward reward received + 0.99 × best guess for the next screen.

## Related notes

- [[Agent Learning Limitations]] — This note describes the agent's learning process and observations.
- [[PacMan DQN Project]] — This note details the specific project where the agent was trained and observed limitations.
- [[Training Results Analysis]] — This note analyzes the quantitative results of the training process.

## Sources

- [[Pac-Man DQN README#5. What the agent sees, does, and is rewarded for (plain language)|Pac-Man DQN README § 5. What the agent sees, does, and is rewarded for (plain language)]] · source S3 · lines 202–216

Original file: `vault/raw/Pac-Man DQN README.md` (unchanged; SHA-256 `605a0ab0e419df4d…`)
