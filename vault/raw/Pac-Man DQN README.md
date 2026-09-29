# Ms. Pac-Man DQN — Class 3 assignment

**Brian Arevalo Ramos · MBA 290T Fundamentals of Agentic AI · Class 3 / Assignment 2**

I trained the course's ready-made Deep Q-Network (DQN) on `ALE/MsPacman-v5` with three choices of my own:
**exploration 0.10, 500 training games, learning rate 0.0001.** Everything below comes from one executed run of
[`pacman_dqn.ipynb`](pacman_dqn.ipynb) on my Intel MacBook Pro (CPU). The notebook is saved **with all cell outputs**
from that final run, and the evidence it produced is copied into [`results/`](results/).

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/BuildingBrian/pacman-dqn/blob/main/pacman_dqn.ipynb)

| | Untrained network | Trained agent |
|---|---|---|
| Mean score over the same 5 evaluation games | **492.0** | **608.0** |
| First 20 s of one evaluation game (4× speed) | ![Untrained gameplay](results/demos/episode_0000.gif) | ![Best trained gameplay](results/demos/final_best.gif) |

Change in mean score: **+116.0**. The five individual scores are in the [results table](#the-five-before-and-after-scores).

---

## 1. Open and run the notebook

**Google Colab (easiest):** click the badge above, choose *Runtime → Change runtime type → T4 GPU* if available,
edit the three values in section 1, then *Runtime → Run all*. The setup cell installs the packages.

**Local Jupyter / VS Code:**

```bash
git clone https://github.com/BuildingBrian/pacman-dqn.git
cd pacman-dqn
python3.12 -m venv .venv && source .venv/bin/activate     # Python 3.11–3.13
pip install -r requirements.txt
jupyter lab pacman_dqn.ipynb                              # then Run All
```

**Exactly how this submission was produced (headless, no browser):**

```bash
source .venv/bin/activate
python -m ipykernel install --user --name pacman-dqn
python tools/run_headless.py --deadline 20:30            # runs every cell in order, saves outputs into the notebook
python tools/collect_results.py pacman_runs/<run folder>  # copies the evidence into results/
```

`tools/run_headless.py` executes the notebook top to bottom with `nbclient` and writes the outputs back into
`pacman_dqn.ipynb`. The optional `--deadline` sends the kernel **one** interrupt at that wall-clock time if
training is still running; the notebook catches it, saves the agent as an *interrupted* run, and continues
to evaluation. The deadline was not reached; training completed on its own.

### Changes outside section 1 (environment only, no learning settings touched)

The notebook could not run unmodified on an Intel Mac, so I made three edits that change nothing about the agent,
the fixed classroom settings, or the evaluation:

| Cell | Change | Why |
|---|---|---|
| Setup (`%pip`) | Platform-aware pins: Intel Macs get `torch==2.2.2`, `numpy<2`, `opencv-python-headless<4.12`; every other platform keeps the original pins | PyTorch stopped publishing x86_64 macOS wheels after 2.2.2, and that version needs NumPy 1.x, which in turn needs an older OpenCV. The original `torch>=2.6` pin has no installable wheel on this machine. |
| Preview settings | `SHOW_POPUPS = False` | The notebook ran headlessly; there is no desktop to open the Tk popup player on. Inline GIFs are still displayed in the notebook (the starter README documents this toggle). |
| `select_device` | Skip MPS on Intel Macs, so the run uses **CPU** | PyTorch no longer maintains the Radeon/Intel MPS path. I benchmarked both on this laptop: about 10 ms per training decision either way, so CPU costs nothing and is reproducible with the fixed seeds. |

[`requirements.txt`](requirements.txt) carries the same platform markers.

---

## 2. My three choices and why

| Setting | My value | Notebook default | Why I chose it |
|---|---|---|---|
| **Exploration** | **0.10** | 0.20 | After the 1,000-decision random warm-up, 10 % of training moves are random. This is the value the original DQN paper anneals *down to*, and it is closer to the fixed 5 % used in evaluation, so the agent trains on behavior that looks like how it will be tested. The environment already injects randomness through 25 % sticky actions and up to 30 random no-ops at reset. With a replay memory of only 5,000 decisions (roughly 5–8 games), what the network learns from is very recent, so I wanted most of that memory to be the agent's own policy rather than coin flips. The risk is the opposite failure: too little exploration can lock in an early habit. |
| **Episodes** | **500** | 100 | Five times the starting value, because the notebook itself warns that useful Atari learning "may require much longer runs". The ceiling was the calendar: the assignment was due the same night. I measured about 16 ms per training decision on this laptop, so 500 games projected to 1.5–4 hours depending on how long the agent survives (a game is capped at 3,000 decisions). I armed a one-shot safety interrupt at 8:30 PM so evaluation and this write-up would always fit before the deadline. |
| **Learning rate** | **0.0001** | 0.0001 | The reference point for Adam in DQN implementations (Stable-Baselines3 defaults to 1e-4; Dopamine uses 6.25e-5). With a tiny replay memory the gradient estimates are noisy, and a bigger step risks the divergence the notebook guards against (it aborts on a non-finite loss). A smaller step would waste the limited episode budget. |

I kept every other setting exactly as shipped: replay capacity 5,000, batch 32, warm-up 1,000, one update every
4 decisions, target sync every 1,000 decisions, gamma 0.99, seed 42, rewards clipped to [-1, 1] for learning.

**Setup check first.** Before the real run I executed the notebook once with the default settings and 5 episodes
(exploration 0.20, learning rate 0.0001). It completed 2,806 decisions and 452 learning updates in 33 seconds and
scored 492 → 408 (mean before → after), which is what a 5-game run should look like: everything works, nothing has
been learned yet. That run is not the submission; it only confirmed the pipeline.

---

## 3. What I expected before training

Written before the 500-episode run started, informed only by the 5-episode setup check:

- **Untrained baseline around 300–800 points per game** (the setup check's untrained network averaged 492). A random
  network still eats pellets because Ms. Pac-Man keeps moving in whatever direction the joystick last said, so "doing
  nothing useful" is worth a few hundred points before the ghosts arrive.
- **Modest, noisy improvement, not mastery.** I expected the trained mean to land somewhere around 600–900: the agent
  should learn that continuing along an unfinished pellet row pays, and that some moves near ghosts end the game. I did
  not expect deliberate ghost avoidance, power-pellet hunting, or clearing a maze, because 500 games is roughly
  1–2 % of the experience the original DQN paper used, and the replay memory here holds 0.5 % of the paper's.
- **A jagged training curve** with a 25-game average that drifts up slowly and can fall back, and **a loss that does not
  simply go down** (as the network's value estimates grow, the targets move with them). The notebook warns that lower
  loss is not the same as better play.
- **Real chance of no improvement or regression** on the five fixed evaluation games, because a constant 10 %
  exploration with a 5,000-decision memory can keep overwriting what was learned a few games ago.

---

## 4. What actually happened

### Training budget that was actually used

| | Value |
|---|---|
| Status | completed |
| Completed training games | 500 of 500 requested |
| Agent decisions (4 game frames each) | 296,988 |
| Learning updates (batches of 32) | 73,998 |
| Elapsed training time (including the every-25-game demos) | 1 h 19 min (79 min) |
| Hardware | Intel Core i7-9750H (6 cores), 32 GB RAM, **CPU** (PyTorch used 4 threads) |
| Software | Python 3.12.14, torch 2.2.2, gymnasium 1.3.0, ale-py 0.11.2, opencv-python-headless 4.11.0.86, numpy 1.26.4, matplotlib 3.11.2, Pillow 12.3.0 |

Source files: [`training_summary.json`](results/training_summary.json) · [`config.json`](results/config.json) ·
[`training.csv`](results/training.csv) (one row per completed game).

The elapsed time is the notebook's own measurement, a monotonic clock that stops while the Mac sleeps. On the wall clock
the run went from 12:51 PM to 2:42 PM PDT: the laptop lid was closed twice and the process sat paused for about
31 minutes in total, then resumed, which does not change any result.

### The five before-and-after scores

Same five seeds (101, 202, 303, 404, 505), same 5 % evaluation exploration, same 3,000-decision cap, before and
after training. The baseline is the **untrained network**, not a random-action agent.

| Game | Seed | Untrained score | Trained score | Change |
|---|---|---|---|---|
| 1 | 101 | 350 | 530 | +180 |
| 2 | 202 | 500 | 520 | +20 |
| 3 | 303 | 320 | 680 | +360 |
| 4 | 404 | 800 | 640 | -160 |
| 5 | 505 | 490 | 670 | +180 |
| **Mean** | | **492.0** | **608.0** | **+116.0** |

Full evaluation record with game lengths: [`comparison.json`](results/comparison.json) ·
[`baseline.json`](results/baseline.json). No game hit the 3,000-decision time limit before or after training; every game ended at game over.

### Training dashboard

![Training dashboard: raw training score, mean update loss, and exploration per completed episode](results/training_dashboard.png)

**Reading the three panels.** *Left:* single training games (light blue) swing between about 100 and 2,910 points;
the 25-game average (orange) jumps from 130 after the first, fully random game into the 600–900 band within 25 games and
then stays there. The first quarter of training averaged 705 points per game and the last quarter 739, with the best
25-game average (912) at game 328 and the two best single games at game 70 (2,640) and game 448 (2,910). So
most of the measurable learning happened early; after that the agent oscillated rather than climbed. *Middle:* the mean
update loss did **not** fall. It rose from 0.024 in game 2 to a peak of 0.200 at game 355 and settled around 0.10–0.12.
That is not by itself a failure: the loss measures the gap between the network's guess and a target built from its own
slowly synced copy, so as the value estimates grow from near zero toward realistic point totals, the targets move and the
gap widens. The notebook's warning that lower loss does not mean better play cuts both ways. *Right:* exploration was
100 % only during the first game, because the 1,000-decision random warm-up ended during game 2; from then on it sat at
exactly 10 %.

### Gameplay: untrained → every 25 games → best trained

Each GIF is the first 20 seconds of one evaluation game on seed 101 at 4× speed (about 5 s to watch), recorded by the
notebook while training continued. The score under each intermediate GIF is that checkpoint's **full** game score on
seed 101 (from [`demo_scores.json`](results/demo_scores.json)), not just the 20 seconds shown.

| Untrained (episode 0) | Best trained game (after training) |
|---|---|
| ![Untrained](results/demos/episode_0000.gif) | ![Best trained](results/demos/final_best.gif) |

| After 25 games | After 50 games | After 75 games | After 100 games | After 125 games |
|---|---|---|---|---|
| ![After 25 games](results/demos/episode_0025.gif) | ![After 50 games](results/demos/episode_0050.gif) | ![After 75 games](results/demos/episode_0075.gif) | ![After 100 games](results/demos/episode_0100.gif) | ![After 125 games](results/demos/episode_0125.gif) |
| seed-101 score **340** | seed-101 score **190** | seed-101 score **380** | seed-101 score **550** | seed-101 score **640** |

| After 150 games | After 175 games | After 200 games | After 225 games | After 250 games |
|---|---|---|---|---|
| ![After 150 games](results/demos/episode_0150.gif) | ![After 175 games](results/demos/episode_0175.gif) | ![After 200 games](results/demos/episode_0200.gif) | ![After 225 games](results/demos/episode_0225.gif) | ![After 250 games](results/demos/episode_0250.gif) |
| seed-101 score **260** | seed-101 score **970** | seed-101 score **400** | seed-101 score **430** | seed-101 score **240** |

| After 275 games | After 300 games | After 325 games | After 350 games | After 375 games |
|---|---|---|---|---|
| ![After 275 games](results/demos/episode_0275.gif) | ![After 300 games](results/demos/episode_0300.gif) | ![After 325 games](results/demos/episode_0325.gif) | ![After 350 games](results/demos/episode_0350.gif) | ![After 375 games](results/demos/episode_0375.gif) |
| seed-101 score **370** | seed-101 score **210** | seed-101 score **500** | seed-101 score **210** | seed-101 score **480** |

| After 400 games | After 425 games | After 450 games | After 475 games | After 500 games |
|---|---|---|---|---|
| ![After 400 games](results/demos/episode_0400.gif) | ![After 425 games](results/demos/episode_0425.gif) | ![After 450 games](results/demos/episode_0450.gif) | ![After 475 games](results/demos/episode_0475.gif) | ![After 500 games](results/demos/episode_0500.gif) |
| seed-101 score **340** | seed-101 score **430** | seed-101 score **440** | seed-101 score **1100** | seed-101 score **530** |

**What the GIFs show.** The untrained network (top left) picks a direction and mostly holds it: in the seed-101 game
Ms. Pac-Man drifts along one corridor eating whatever pellets are in the way and has 350 points when the 20-second
excerpt ends, which is also its final score for that game, so the ghosts caught it soon after. The best trained game
(top right, seed 303, 680 points) sweeps the left-hand corridors more deliberately and has 360 points at the 20-second
mark, on its way to more than doubling the untrained total on that seed (320 → 680). The twenty intermediate GIFs are the
more sobering evidence: the same seed-101 game scores anywhere between 190 (after 50 games) and 1,100 (after 475 games)
with no steady climb, so the policy that exists after any given 25 games is materially different from the one 25 games
earlier. The most telling number is not in the GIFs at all. The trained agent's five evaluation games were **not longer**
than the untrained ones (571 vs 589 decisions on average; every one of the ten games ended by losing all lives, none
reached the 3,000-decision cap), but they scored **more per decision** (1.06 vs 0.84 points). The agent learned to eat
faster, not to survive longer.

---

## 5. What the agent sees, does, and is rewarded for (plain language)

- **Observations — four game screens.** Each decision, the agent does not see the colorful Atari frame. It sees the last
  four screens shrunk to 84 × 84 grayscale pixels and stacked together. One screen shows *where* everything is; four in a
  row show *which way* everything is moving. That is the entire input: no maze map, no ghost coordinates, no score.
- **Actions — joystick moves.** The network outputs nine numbers, one per joystick position: no-op, up, right, left,
  down, and the four diagonals. Each number is the network's *guess* at how many future points that move leads to.
  Most of the time the agent takes the highest guess; 10 % of the time during training (5 % during evaluation) it picks
  a random move instead. One decision holds the joystick for four game frames.
- **Rewards — game points.** The game itself supplies the reward: the change in score after each decision (10 for a
  pellet, 50 for a power pellet, 200+ for a ghost, fruit bonuses). For learning, each reward is clipped to between -1 and
  +1 so a ghost is not a hundred times "louder" than a pellet; every score reported here is the raw game score. Dying is
  not punished directly; the agent only "feels" it as the future points that never arrive.
- **How it learns.** The agent stores its last 5,000 decisions and, every four decisions, replays 32 random ones,
  nudging its guesses toward *reward received + 0.99 × best guess for the next screen* (that next-screen guess comes from
  a slower-changing copy of the network so the target does not chase itself). Game over sets the future term to zero; hitting
  the 3,000-decision time cap does not.

---

## 6. One limitation I observed

**The agent did not learn to avoid ghosts, and 500 games with a 5,000-decision memory were not enough to expect it to.**
Trained games were no longer than untrained games (571 vs 589 decisions), the seed-101 checkpoint score swung between
190 and 1,100 with no trend, and the 25-game average plateaued after roughly game 25. Two design choices in this
classroom DQN explain most of that. First, the replay memory holds about eight games, so every update is drawn from the
agent's most recent behavior and older lessons are overwritten (the original DQN paper kept 1,000,000 transitions).
Second, losing a life carries no negative reward, so a death only shows up indirectly as future points that never
arrive, a weak signal when the future is discounted by 0.99 per decision and every reward is clipped to ±1. A smaller
but real caveat on the headline number: five evaluation games is a small sample, and one of the five (seed 404) got
*worse* (800 → 640), so the +116 mean improvement is real for this run but should not be read as a precise measure of
the agent's skill.

## 7. Next experiment (change exactly one setting)

**Change one setting: replay capacity 5,000 → 50,000, keeping exploration 0.10, 500 episodes, and learning rate 0.0001
exactly as they were.** The failure I observed was forgetting, not slowness: the agent reached its plateau within 25
games and then cycled, and the every-25-game checkpoints behaved like different agents. A ten-times-larger memory (about
1.7 GB of pixels, which fits in this laptop's 32 GB) would let each batch of 32 mix experiences from roughly 80 games
instead of 8, which is the mechanism the DQN paper relies on to stabilize learning. My prediction: the 25-game average
should keep rising past the 912 ceiling instead of oscillating around 700, the seed-101 checkpoint scores should stop
swinging by a factor of five, and trained games should finally get *longer* than untrained ones. Of the three student
choices, I would leave all three alone for that run: more episodes with the same small memory would mostly repeat the
same cycle, and exploration and learning rate are hard to judge until the memory stops erasing what they produce. If the
larger memory works, the run after that would be 1,500–2,000 episodes overnight.

---

## 8. Evidence index

| Evidence | Where |
|---|---|
| Executed notebook with all outputs from the final run | [`pacman_dqn.ipynb`](pacman_dqn.ipynb). GitHub's notebook preview renders the printed scores and the dashboard PNG, but shows GIF outputs as `<IPython.core.display.Image object>`; the same GIFs are embedded above from `results/demos/` and render in Jupyter or Colab. |
| Settings, hardware, package versions | [`results/config.json`](results/config.json) |
| One row per completed training game | [`results/training.csv`](results/training.csv) |
| Completed episodes, decisions, learning updates, elapsed time, status | [`results/training_summary.json`](results/training_summary.json) |
| All five untrained and trained evaluation scores, game lengths, time-limit flags | [`results/comparison.json`](results/comparison.json) |
| Untrained evaluation on its own | [`results/baseline.json`](results/baseline.json) |
| Every-25-game demo scores | [`results/demo_scores.json`](results/demo_scores.json) |
| Training dashboard (score, loss, exploration) | [`results/training_dashboard.png`](results/training_dashboard.png) |
| Untrained, intermediate, and best trained GIFs | [`results/demos/`](results/demos/) |
| Headless runner and evidence collector | [`tools/`](tools/) |

**Interrupted run or no learning updates?** No. The run **completed** all requested episodes, and learning updates were performed (see the count above), so this is neither an interrupted run nor a run without learning.

**Model checkpoints.** The run folder `pacman_runs/20260915_125127_421799/` and its ZIP hold `untrained.pt`, `trained.pt`, and a
checkpoint every 25 games. They are gitignored (each is about 6.4 MB) and kept locally; the complete run ZIP (138 MB: all 22 checkpoints plus every file now in `results/`) is attached to the GitHub release
**[run-2026-09-15](https://github.com/BuildingBrian/pacman-dqn/releases/tag/run-2026-09-15)**.

---

## Sources

- Course starter repository: [pepealonso95/pacman-dqn](https://github.com/pepealonso95/pacman-dqn)
- [DQN paper: Human-level control through deep reinforcement learning](https://storage.googleapis.com/deepmind-media/dqn/DQNNaturePaper.pdf)
- [ALE installation and Gymnasium registration](https://ale.farama.org/getting-started/)
- [Gymnasium Atari preprocessing](https://gymnasium.farama.org/api/wrappers/misc_wrappers/#gymnasium.wrappers.AtariPreprocessing)
- [Gymnasium frame stacking](https://gymnasium.farama.org/api/wrappers/observation_wrappers/#gymnasium.wrappers.FrameStackObservation)
