---
title: Training Results Analysis
folder: Results
source_id: S3
source_file: raw/Pac-Man DQN README.md
source_sha256: 605a0ab0e419df4d
source_sections:
  - "3. What I expected before training"
  - "4. What actually happened > Training budget that was actually used"
  - "4. What actually happened > The five before-and-after scores"
  - "4. What actually happened > Training dashboard"
  - "4. What actually happened > Gameplay: untrained → every 25 games → best trained"
generated_by: gemma4:e2b Q4_K_M (Ollama 0.20.7, local)
generated_at: 2026-09-29
reviewed: false
---

# Training Results Analysis

The training process involved 500 completed games and resulted in an average score increase of 116.0 across five seeds. The learning appeared to happen early in the training, with the best results observed in the first quarter.

## Key details

- Completed training games was 500 of 500 requested.
- Agent decisions were 296,988.
- Learning updates were 73,998 batches of 32.
- The elapsed training time was 1 h 19 min (79 min).
- The mean score change was +116.0.
- The best 25-game average score was 912 at game 328.
- The best single game scores were 2,640 at game 70 and 2,910 at game 448.

## Related notes

- [[PacMan DQN Project]] — The training results analysis summarizes the outcome of the PacMan DQN project.
- [[Initial Expectations]] — Initial expectations describe the author's predictions about the learning process that the training results are being analyzed against.
- [[Agent Learning Limitations]] — Agent learning limitations describe the specific failures and instability observed during the training process mentioned in the results.

## Sources

- [[Pac-Man DQN README#3. What I expected before training|Pac-Man DQN README § 3. What I expected before training]] · source S3 · lines 85–98
- [[Pac-Man DQN README#Training budget that was actually used|Pac-Man DQN README § Training budget that was actually used]] · source S3 · lines 106–121
- [[Pac-Man DQN README#The five before-and-after scores|Pac-Man DQN README § The five before-and-after scores]] · source S3 · lines 125–138
- [[Pac-Man DQN README#Training dashboard|Pac-Man DQN README § Training dashboard]] · source S3 · lines 144–154
- [[Pac-Man DQN README#Gameplay: untrained → every 25 games → best trained|Pac-Man DQN README § Gameplay: untrained → every 25 games → best trained]] · source S3 · lines 158–196

Original file: `vault/raw/Pac-Man DQN README.md` (unchanged; SHA-256 `605a0ab0e419df4d…`)
