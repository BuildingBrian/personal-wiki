# Choices and expectations, written before testing

Written 2026-09-29 before the retrieval and harness code existed (see the git history: this file and
`questions.json` are in the first commit, the code is not).

## My three choices

**Data.** The wiki is a memory of my own projects in MBA 290T: what I built, what I measured, what failed, and what I
said I would try next. Sources are the three README files I wrote for earlier assignments (custom LLM, Pac-Man DQN,
networking tracker). They are already public in my own repositories, so they are shareable, and I know their content
well enough to check every answer. Scope is deliberately small: three documents, about 17,000 words.

**Model.** `gemma4:e2b`, quantization Q4_K_M, running in Ollama 0.20.7 on CPU. My laptop is a 2019 Intel MacBook Pro
(i7-9750H, 32 GB RAM); its Radeon GPU is not used by the runtime. E2B is the smallest Gemma, which matters on CPU
because reading speed, not memory, is my bottleneck. I measured it before building: about 42 tokens/s reading the
prompt, about 15 to 17 tokens/s writing, 7.7 GB loaded, 11 s cold load. A 3,000-token prompt takes 72 s to read, so
the harness must keep prompts near 1,000 tokens.

**Retrieval.** A local keyword index (BM25) over passages of the original sources, built with the Python standard
library only. No embedding model, no hosted API, nothing to download at question time. Passages are about 130 words,
cut at headings and paragraph boundaries, and each keeps its source path, section and line numbers.

## What I expect

| Test | Retrieval prediction | Answer prediction |
|---|---|---|
| 1 Pac-Man mean score | The score table is retrieved at rank 1 or 2: "mean", "score", "trained", "untrained" all appear in it. | Correct numbers with a citation. Risk: the model reads the wrong row of the table. |
| 2 Skill the language model failed | **Most likely to fail.** Keyword search matches words, not meaning: the question never says "negation", and "language" and "model" appear in almost every passage of that README, so they carry little signal. I expect the right passage to be outside the top ranks. | If retrieval misses, the model should say insufficient evidence rather than guess. |
| 3 Networking tracker privacy | Retrieved at rank 1 to 3; "contacts" and "user" are distinctive for that source. | Correct, citing Row Level Security. |
| 4 GPU purchase (unsupported) | The "considering hardware for training at home" paragraph is retrieved, because it shares "GPU", "train", "models", "home". | The hard part. A small model may turn "considering hardware" into a purchase. Expected behavior is an explicit insufficient-evidence statement. |

**Mode boundaries.** Chat should answer "what can you help me with?" from its persona without searching notes.
"make that shorter" should use the conversation. Search should print passages and never call the model. A claim made
only in chat must not be treated as evidence by ask.

**Speed.** About 30 s per ask answer (1,000 tokens read, about 80 written). Ingestion is the slow step: about one
minute per wiki note.
