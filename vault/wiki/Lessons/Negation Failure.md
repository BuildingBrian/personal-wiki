---
title: Negation Failure
folder: Lessons
source_id: S1
source_file: raw/Custom LLM README.md
source_sha256: c8971e5d4ef04c14
source_sections:
  - "4. The fixed 48-case language evals > 4.3 Reading the results honestly"
  - "7. One limitation and my next experiment"
generated_by: gemma4:e2b Q4_K_M (Ollama 0.20.7, local)
generated_at: 2026-09-29
reviewed: true
reviewed_by: Brian Arevalo Ramos, with Claude (AI assistant)
reviewed_at: 2026-09-29
---

# Negation Failure

Negation transfer failed, resulting in a success rate of 1/3, which is equivalent to chance. The model learned the surface shape of the correction stories but picked the negated word, or an unrelated one, instead of the corrected word.

## Key details

- Negation transfer resulted in 1/3 success, which is chance.
- For `lang_32` ("ava did not buy tea . she bought milk . ava bought"), the model chose the negated word, `tea`.
- For `lang_31`, the model chose `green`, a colour that never appears in the prompt.
- Only `lang_33` was correct in this instance.
- The model learned the shape "X is not A . it is B . X is" but not which of A or B to copy.
- Copying the right earlier token requires attention to the position after "it is" / "she bought".
- 620 stories × 3,000 steps did not produce the required copying pattern.
- My next experiment changes only the negation data: roughly triple it to about 2,000 stories and vary the frames, keeping steps, learning rate and the other files fixed.

## Related notes

- [[Custom LLM Eval Results]] — Gives the scores by category, where negation is the only taught category at chance.
- [[Custom LLM Training Choices]] — Gives the prediction I wrote before training, which expected negation to stay near chance.
- [[Eval Leakage Policy]] — Explains why this was a fair test: the correction pairs in the evals never appear in my corpus.
- [[Pac-Man Agent Limitation]] — Describes the limitation I found in my Pac-Man agent and the one-setting experiment proposed to fix it.

## Sources

- [[Custom LLM README#4.3 Reading the results honestly|Custom LLM README § 4.3 Reading the results honestly]] · source S1 · lines 399–424
- [[Custom LLM README#7. One limitation and my next experiment|Custom LLM README § 7. One limitation and my next experiment]] · source S1 · lines 519–528

Original file: `vault/raw/Custom LLM README.md` (unchanged; SHA-256 `c8971e5d4ef04c14…`)
