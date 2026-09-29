---
title: Pac-Man Gameplay Progress
folder: Results
source_id: S3
source_file: raw/Pac-Man DQN README.md
source_sha256: 605a0ab0e419df4d
source_sections:
  - "4. What actually happened > Gameplay: untrained → every 25 games → best trained"
generated_by: gemma4:e2b Q4_K_M (Ollama 0.20.7, local)
generated_at: 2026-09-29
reviewed: true
reviewed_by: Brian Arevalo Ramos, with Claude (AI assistant)
reviewed_at: 2026-09-29
---

# Pac-Man Gameplay Progress

Every 25 training games the notebook recorded one full game on seed 101. The scores swing between 190 and 1,100 with no steady climb.

## Key details

- The untrained network scored 350 on seed 101.
- After 25 games, the score for seed-101 is 340.
- After 50 games, the score for seed-101 is 190.
- After 75 games, the score for seed-101 is 380.
- After 100 games, the score for seed-101 is 550.
- After 125 games, the score for seed-101 is 640.
- After 150 games, the score for seed-101 is 260.
- After 175 games, the score for seed-101 is 970.
- Later checkpoints kept swinging: 400, 430, 240, 370, 210, 500, 210, 480, 340, 430, 440, then 1,100 after 475 games and 530 after 500.
- Trained games were not longer than untrained ones (571 vs 589 decisions) but scored more per decision (1.06 vs 0.84 points): the agent learned to eat faster, not to survive longer.

## Related notes

- [[Pac-Man Training Results]] — Shows the results of completing training games and the change in mean scores.
- [[Pac-Man Agent Limitation]] — Shows why the gameplay progress does not result in a steady score climb.

## Sources

- [[Pac-Man DQN README#Gameplay untrained → every 25 games → best trained|Pac-Man DQN README § Gameplay: untrained → every 25 games → best trained]] · source S3 · lines 158–196

Original file: `vault/raw/Pac-Man DQN README.md` (unchanged; SHA-256 `605a0ab0e419df4d…`)
