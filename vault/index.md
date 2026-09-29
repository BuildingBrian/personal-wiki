# Project Wiki

This wiki is my memory of the projects I built in MBA 290T: what I built, what I measured, what failed, and what I said I would try next. Notes are drafted by a local Gemma model from my own write-ups and reviewed by me against the originals. Every note links back to the passage it came from.

21 notes from 3 sources. Start with a topic below, open a note, then follow its **Sources** link to the original passage.

## Projects

What each project is and how it was built.

- [[Building Custom LLM With NanoGPT]] — This document details the process of building a custom Large Language Model using nanoGPT.
- [[Custom LLM Chat Interface]] — The chat interface uses the instructor's terminal loop `chat.py` to load weights and vocabulary from `model.pt`.
- [[Networking Tracker Architecture]] — The architecture separates the frontend (React client components) from the backend (Next.js Route Handlers) which interact with the database.
- [[Networking Tracker Database]] — This document describes the database schema for the Networking Tracker.
- [[Networking Tracker Deployment]] — This document details the production verification and deployment process for the Networking Tracker application.
- [[Networking Tracker Features]] — The Networking Tracker features include secure authentication, a private contact list, detailed contact management, and robust sorting and filtering capabilities.
- [[Networking Tracker Overview]] — The Networking Tracker is a private, per-user networking tracker for people at Berkeley.
- [[Networking Tracker Request Flow]] — This document outlines the end-to-end request flow for adding, reading, updating, and deleting contacts.
- [[Networking Tracker Testing]] — The project has two test suites, totaling 25 tests, which are executed via `npm test`.

## Results

What was measured, with the numbers.

- [[Custom LLM Evidence From Network]] — This document details various measurements and observations from a Custom LLM, including loss curves, sample generation, token-to-ID mapping, weight updates, next-token probabilities, attention patterns, and temperature effects.
- [[Custom LLM Language Evals]] — The system uses fixed 48-case language evaluations where each case consists of a prompt, four single-word choices, and one answer.
- [[Initial Expectations]] — The initial expectations were based on a 5-episode setup check and predictions about the learning process.
- [[LLM Results At A Glance]] — This table provides a glance at the results from different experiments involving language evaluations.
- [[Training Results Analysis]] — The training process involved 500 completed games and resulted in an average score increase of 116.0 across five seeds.

## Concepts

Ideas and mechanisms the projects rely on.

- [[Agent Observations And Rewards]] — The agent observes four game screens, takes joystick moves, and is rewarded based on changes in game score.
- [[LLM Concepts And Mechanisms]] — The text describes two experiments involving different corpora to train a model, focusing on word associations, categories, and negation.
- [[PacMan DQN Project]] — The PacMan DQN project involved training an agent using specific settings and observed limitations regarding learning ghosts and memory.

## Lessons

What failed, what I learned, and what I would try next.

- [[Agent Learning Limitations]] — The agent failed to learn to avoid ghosts, and the training process showed unstable results.
- [[Custom LLM Lessons Learned]] — The custom LLM learned to associate word relationships and template shapes rather than memorizing specific sentences or facts.
- [[Experiment Next Steps]] — The next experiment involves changing exactly one setting to test the effect of replay capacity.
- [[Networking Tracker Limitations]] — The Networking Tracker has several known limitations that could be improved.

## Source catalog

Originals live unchanged in `raw/`. The id is what evidence files and note properties refer to.

| ID | Source | Original file | Origin | Words | SHA-256 | Added |
|---|---|---|---|---|---|---|
| S1 | [[Custom LLM README]] | `README.md` | github.com/BuildingBrian/custom-llm @ 3854cd2 | 8168 | `c8971e5d4ef0…` | 2026-09-29 |
| S2 | [[Networking Tracker README]] | `README.md` | github.com/BuildingBrian/networking-tracker @ 556f732 | 4153 | `791a30402c37…` | 2026-09-29 |
| S3 | [[Pac-Man DQN README]] | `README.md` | github.com/BuildingBrian/pacman-dqn @ 4c476c9 | 3186 | `605a0ab0e419…` | 2026-09-29 |
