# Evidence card: test-1

- **Mode:** ask (standalone, no chat history) · **Execution:** local
- **Recorded:** 2026-09-29 17:26:24 PDT · **Network:** connected (Wi-Fi On, default route True, outside host answered True)
- **Model:** gemma4:e2b · 5.1B · Q4_K_M · digest 7fbdbf8f5e45 · Ollama 0.20.7
- **Model memory:** 7.68 GB loaded, 100% CPU

## Question

What was the mean evaluation score of the Pac-Man agent before and after training?

## Expected (written before the harness existed)

- Kind: answerable — Direct question answered by one source.
- Expected source: `vault/raw/Pac-Man DQN README.md` › The five before-and-after scores
- Expected answer: Mean of the five fixed evaluation games: 492.0 untrained, 608.0 trained (+116.0).

## Retrieved passages

Query terms: `mean, evalu, score, pac, man, agent, train`

### [1] `vault/raw/Pac-Man DQN README.md` › Ms. Pac-Man DQN — Class 3 assignment (lines 3–17)
score 21.27 · matched: mean, evalu, score, pac, man, agent, train · found via keyword

> **Brian Arevalo Ramos · MBA 290T Fundamentals of Agentic AI · Class 3 / Assignment 2**
> 
> I trained the course's ready-made Deep Q-Network (DQN) on `ALE/MsPacman-v5` with three choices of my own:
> **exploration 0.10, 500 training games, learning rate 0.0001.** Everything below comes from one executed run of
> [`pacman_dqn.ipynb`](pacman_dqn.ipynb) on my Intel MacBook Pro (CPU). The notebook is saved **with all cell outputs**
> from that final run, and the evidence it produced is copied into [`results/`](results/).
> 
> [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/BuildingBrian/pacman-dqn/blob/main/pacman_dqn.ipynb)
> 
> | | Untrained network | Trained agent |
> |---|---|---|
> | Mean score over the same 5 evaluation games | **492.0** | **608.0** |
> | First 20 s of one evaluation game (4× speed) | ![Untrained gameplay](results/demos/episode_0000.gif) | ![Best trained gameplay](results/demos/final_best.gif) |
> 
> Change in mean score: **+116.0**. The five individual scores are in the [results table](#the-five-before-and-after-scores).

### [2] `vault/raw/Pac-Man DQN README.md` › 4. What actually happened > The five before-and-after scores (lines 125–138)
score 13.11 · matched: mean, evalu, score, agent, train · found via keyword

> Same five seeds (101, 202, 303, 404, 505), same 5 % evaluation exploration, same 3,000-decision cap, before and
> after training. The baseline is the **untrained network**, not a random-action agent.
> 
> | Game | Seed | Untrained score | Trained score | Change |
> |---|---|---|---|---|
> | 1 | 101 | 350 | 530 | +180 |
> | 2 | 202 | 500 | 520 | +20 |
> | 3 | 303 | 320 | 680 | +360 |
> | 4 | 404 | 800 | 640 | -160 |
> | 5 | 505 | 490 | 670 | +180 |
> | **Mean** | | **492.0** | **608.0** | **+116.0** |
> 
> Full evaluation record with game lengths: [`comparison.json`](results/comparison.json) ·
> [`baseline.json`](results/baseline.json). No game hit the 3,000-decision time limit before or after training; every game ended at game over.

### [3] `vault/raw/Pac-Man DQN README.md` › 3. What I expected before training (lines 87–98)
score 12.71 · matched: mean, pac, man, agent, train · found via keyword

> - **Untrained baseline around 300–800 points per game** (the setup check's untrained network averaged 492). A random
>   network still eats pellets because Ms. Pac-Man keeps moving in whatever direction the joystick last said, so "doing
>   nothing useful" is worth a few hundred points before the ghosts arrive. - **Modest, noisy improvement, not mastery.** I expected the trained mean to land somewhere around 600–900: the agent
>   should learn that continuing along an unfinished pellet row pays, and that some moves near ghosts end the game. I did
>   not expect deliberate ghost avoidance, power-pellet hunting, or clearing a maze, because 500 games is roughly
>   1–2 % of the experience the original DQN paper used, and the replay memory here holds 0.5 % of the paper's. - **A jagged training curve** with a 25-game average that drifts up slowly and can fall back, and **a loss that does not
>   simply go down** (as the network's value estimates grow, the targets move with them).

### [4] `vault/raw/Pac-Man DQN README.md` › 5. What the agent sees, does, and is rewarded for (plain language) (lines 202–216)
score 9.52 · matched: evalu, score, agent, train · found via wiki note: Pac-Man DQN Project

> - **Observations — four game screens.** Each decision, the agent does not see the colorful Atari frame. It sees the last
>   four screens shrunk to 84 × 84 grayscale pixels and stacked together. One screen shows *where* everything is; four in a
>   row show *which way* everything is moving. That is the entire input: no maze map, no ghost coordinates, no score. - **Actions — joystick moves.** The network outputs nine numbers, one per joystick position: no-op, up, right, left,
>   down, and the four diagonals. Each number is the network's *guess* at how many future points that move leads to. Most of the time the agent takes the highest guess; 10 % of the time during training (5 % during evaluation) it picks
>   a random move instead. One decision holds the joystick for four game frames.

## Actual answer

**Status:** answered

[1] The mean score over the same five evaluation games for the untrained network was 492.0, and for the trained agent was 608.0 [1]. The change in mean score was +116.0 [1].

## Citation check (done by the harness)

- Cited passages: [1] · valid: [1] · not retrieved: []
- Figures in the answer: ['116.0', '492.0', '608.0']
- Figures missing from the cited passages: []

## Timing

50.49 s total · prompt 1565 tokens at 46.6 tokens/s · answer 55 tokens at 14.1 tokens/s

## Automatic checks

- Passage containing all expected strings ['492.0', '608.0']: rank [1, 2]
- Passage from the expected section "The five before-and-after scores": rank [2]

## My assessment

_to be written after reading the cited passages_
