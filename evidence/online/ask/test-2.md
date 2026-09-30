# Evidence card: test-2

- **Mode:** ask (standalone, no chat history) · **Execution:** local
- **Recorded:** 2026-09-29 17:26:59 PDT · **Network:** connected (Wi-Fi On, default route True, outside host answered True)
- **Model:** gemma4:e2b · 5.1B · Q4_K_M · digest 7fbdbf8f5e45 · Ollama 0.20.7
- **Model memory:** 7.68 GB loaded, 100% CPU

## Question

Which skill did my tiny language model fail to pick up, and what wrong word did it choose?

## Expected (written before the harness existed)

- Kind: answerable — Phrased differently from the source, to see how retrieval handles wording. The source says 'negation', 'failure', 'chose tea, the negated word'; the question says none of those except 'choose'.
- Expected source: `vault/raw/Custom LLM README.md` › 4.3 Reading the results honestly
- Expected answer: Negation (1 of 3, chance). On the 'ava did not buy tea' case it chose 'tea', the negated word.

## Retrieved passages

Query terms: `skill, tiny, language, model, fail, pick, wrong, word, choose`

### [1] `vault/raw/Custom LLM README.md` › 5. Chat interface (lines 451–467)
score 9.28 · matched: tiny, language, model, word · found via keyword

> **Interface:** the instructor's terminal loop [`chat.py`](chat.py) (unchanged) loading my Experiment 2 weights and vocabulary
> from `model.pt`. It is a tiny language model: it *continues* a prompt rather than answering it, each prompt starts with a fresh
> context (no conversation memory), unknown words are reported and mapped to `<UNK>`, and only the last 48 tokens of a long prompt are used.
> Generating replies never updates weights or touches the corpus.
> 
> **Launch (from the repo root, after the setup in section 8):**
> 
> ```bash
> .venv/bin/python chat.py --model evidence/expanded/model.pt --transcript my_chat.json
> ```
> 
> Type a prompt, press Enter, type `/quit` to exit; the transcript is saved to the named file.
> 
> **Model / run identity:** `llm_runs/20260922T044308_125561Z` (Experiment 2, 3,000 steps), model sha256 `5593b08e1e84afcc7a136b720178e4af76c4e360032c587074677d9d3066a2a3`.
> 
> **Transcript** ([chat_transcript_terminal.json](evidence/expanded/chat_transcript_terminal.json), temperature 0.8, max 24 tokens, seeds 2026+turn):
> 
> | # | Prompt | Model reply | Unknown words |
> |---|---|---|---|

### [2] `vault/raw/Custom LLM README.md` › 4. The fixed 48-case language evals > 4.3 Reading the results honestly (lines 399–424)
score 9.24 · matched: language, model, pick, word · found via keyword

> she bought milk . ava bought") → the model
>   chose **tea**, the negated word, i.e. it copied the first noun instead of the corrected one. `lang_31` chose `green`, a colour
>   that never appears in the prompt. Only `lang_33` was right. The free continuations agree it is not a fluke: for `lang_31`
>   it generated "not grey ." Given the corpus, the model learned the *shape* "X is not A . it is B . X is" but not which of A or B
>   to copy — with only 620 short stories and 2 layers, "attend back to the word after *it is*" did not emerge. Section 7 proposes the fix. * **Multiple choice ≠ free text.** `lang_30` ("the opposite of noisy is") picks `quiet` correctly among four choices, but its free
>   continuation was "therapist ." — a starter word.

### [3] `vault/raw/Custom LLM README.md` › 7. One limitation and my next experiment (lines 519–528)
score 8.66 · matched: model, fail, pick, word · found via keyword

> **Observed limitation.** Negation transfer failed (1/3, chance). The model learned the surface shape of the correction stories but,
> faced with a new noun, it picked the *negated* word (`tea`) or an unrelated colour (`green`) rather than the corrected one. Copying
> the right earlier token requires attention to key on the position after "it is" / "she bought", and 620 stories × 3,000 steps did not
> produce that. A second, structural limitation: 15 of 48 evals stayed unscorable because the vocabulary is only what the corpus contains.
> 
> **Next experiment (one change).** Keep steps, learning rate and the other files fixed, and change only the negation data: roughly
> triple it (≈2,000 stories) and vary the frames so the correct word is not always in the same position (e.g. "the cup is blue , not red .
> the cup is", "it is green , not white , so the cup is"). Prediction: negation rises from 1/3 to 2/3 or 3/3 if the copying pattern is
> learnable at this size, and stays at chance if the limit is the 2-layer architecture rather than the data. Either outcome is informative;
> the second would motivate a further experiment with 4 layers.

### [4] `vault/raw/Custom LLM README.md` › 5. Chat interface (lines 479–486)
score 3.38 · matched: model, word · found via wiki note: Custom LLM Chat Interface

> **Screenshot** of the session in macOS Terminal, taken by me on 2026-09-22 (the six prompts were typed into the unchanged `chat.py` by [`tools/chat_demo.py`](tools/chat_demo.py); replies are identical to the transcript because each turn's sampling seed is fixed). The bracketed line after *Saved transcript* comes from the small launcher script that opened the window and tried, without permission, to capture it — it is not output of `chat.py`.
> 
> **Observed limitations:** turn 5 is the clearest one — every content word in "my laptop crashed yesterday" is outside the
> vocabulary, so the model received `<UNK> <UNK> <UNK> yesterday` and produced an empty reply. Turn 6 shows what happens with
> partial coverage: three unknown words plus `today` yield a grammatical-looking but meaningless string. Turns 2–4 show the
> taught patterns transferring to prompts that are not in the corpus ("tall"→"short", "trout"→"fish", "the cup … green").

## Actual answer

**Status:** answered

Negation transfer failed [3]. The model picked the negated word, such as "tea", instead of the corrected one, or an unrelated color like "green" [3].

## Citation check (done by the harness)

- Cited passages: [3] · valid: [3] · not retrieved: []
- Figures in the answer: []
- Figures missing from the cited passages: []

## Timing

34.47 s total · prompt 1565 tokens at 50.1 tokens/s · answer 37 tokens at 14.2 tokens/s

## Automatic checks

- Passage containing all expected strings ['Negation', 'tea']: rank [3]
- Passage from the expected section "4.3 Reading the results honestly": rank [2]

## My assessment

_to be written after reading the cited passages_
