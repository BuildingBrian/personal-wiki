# Project Wiki

This wiki is my memory of the projects I built in MBA 290T: what I built, what I measured, what failed, and what I said I would try next. Notes are drafted by a local Gemma model from my own write-ups and reviewed by me against the originals. Every note links back to the passage it came from.

22 notes from 3 sources. Start with a topic below, open a note, then follow its **Sources** link to the original passage.

## Projects

What each project is and how it was built.

- [[Custom LLM Chat Interface]] — I use the instructor's terminal loop, `chat.py`, as my chat interface to interact with my tiny language model.
- [[Custom LLM Project]] — I trained Andrej Karpathy's nanoGPT twice on my Intel MacBook's CPU for an assignment.
- [[Custom LLM Training Choices]] — I made three choices before training: the corpus, 3,000 training steps and a learning rate of 0.001.
- [[Networking Tracker Architecture]] — I designed a networking tracker using a Next.js stack to keep the frontend and backend in one repository.
- [[Networking Tracker Deployment]] — I outline the steps I take to deploy the Networking Tracker.
- [[Networking Tracker Overview]] — I have created a private, per-user networking tracker for people I want to stay connected with at Berkeley.
- [[Pac-Man DQN Project]] — I trained a Deep Q-Network (DQN) on `ALE/MsPacman-v5` for a class assignment.
- [[Pac-Man Training Choices]] — I made three specific choices for my Pac-Man training: Exploration, Episodes, and Learning rate.

## Results

What was measured, with the numbers.

- [[Custom LLM Eval Results]] — I ran the same fixed 48-case eval suite before and after training in both experiments.
- [[Custom LLM Training Evidence]] — I have documented evidence regarding my custom LLM training, focusing on loss curves, weight updates, and next-token probabilities.
- [[Networking Tracker Testing]] — I have conducted testing on my networking tracker, involving two test suites and production verification.
- [[Pac-Man Gameplay Progress]] — Every 25 training games the notebook recorded one full game on seed 101.
- [[Pac-Man Training Results]] — I completed all 500 requested training games in 79 minutes on CPU.

## Concepts

Ideas and mechanisms the projects rely on.

- [[Eval Leakage Policy]] — I implemented a policy to prevent leakage of evaluation material into my training data.
- [[Row Level Security]] — I implement Row Level Security (RLS) on the `contacts` table to control row access based on user authentication.
- [[Sampling Temperature]] — I experimented with three different temperatures for inference, keeping the model, start token, and seed the same.
- [[Tokens And Embeddings]] — I use a process to convert one word from text into an ID and then into a 64-number vector.

## Lessons

What failed, what I learned, and what I would try next.

- [[Custom LLM Lessons Learned]] — I learned about the components and processes involved in training my custom LLM.
- [[Negation Failure]] — Negation transfer failed, resulting in a success rate of 1/3, which is equivalent to chance.
- [[Networking Tracker Limitations]] — I have identified several known limitations in my Networking Tracker.
- [[Next Steps And Hardware]] — I plan to continue experimenting with this notebook and expand my work into visual learning models.
- [[Pac-Man Agent Limitation]] — I observed that the agent did not learn to avoid ghosts, and 500 games with a 5,000-decision memory were insufficient for learning.

## Source catalog

Originals live unchanged in `raw/`. The id is what evidence files and note properties refer to.

| ID | Source | Original file | Origin | Words | SHA-256 | Added |
|---|---|---|---|---|---|---|
| S1 | [[Custom LLM README]] | `README.md` | github.com/BuildingBrian/custom-llm @ 3854cd2 | 8168 | `c8971e5d4ef0…` | 2026-09-29 |
| S2 | [[Networking Tracker README]] | `README.md` | github.com/BuildingBrian/networking-tracker @ 556f732 | 4153 | `791a30402c37…` | 2026-09-29 |
| S3 | [[Pac-Man DQN README]] | `README.md` | github.com/BuildingBrian/pacman-dqn @ 4c476c9 | 3186 | `605a0ab0e419…` | 2026-09-29 |
