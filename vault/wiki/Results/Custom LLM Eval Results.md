---
title: Custom LLM Eval Results
folder: Results
source_id: S1
source_file: raw/Custom LLM README.md
source_sha256: c8971e5d4ef04c14
source_sections:
  - "Results at a glance"
  - "4. The fixed 48-case language evals > 4.1 Scores by group and category"
generated_by: gemma4:e2b Q4_K_M (Ollama 0.20.7, local)
generated_at: 2026-09-29
reviewed: true
reviewed_by: Brian Arevalo Ramos, with Claude (AI assistant)
reviewed_at: 2026-09-29
---

# Custom LLM Eval Results

I ran the same fixed 48-case eval suite before and after training in both experiments. The score rose from 20 to 30 correct once my teaching files were added.

## Key details

- For the starter corpus, I achieved 20 correct out of 48 and 24 scorable out of 48 when trained for 3,000 steps.
- For the expanded corpus, I achieved 30 correct out of 48 and 33 scorable out of 48 when trained for 3,000 steps.
- The jump from 20 to 30 correct came from new vocabulary making 9 more cases scorable and learned patterns answering 7 of those 9.
- The negation category remained at chance with 1/3 success.
- For the starter corpus, the all-case success rate was 41.7% when trained.
- For the expanded corpus, the all-case success rate was 62.5% when trained.
- Untrained, the scores were 9 of 48 (starter corpus) and 12 of 48 (expanded corpus), which is what chance looks like.

## Related notes

- [[Custom LLM Training Choices]] — Gives the corpus, steps and learning rate behind these scores, and what I predicted they would be.
- [[Negation Failure]] — Explains the one taught category that stayed at chance, and the wrong words the model chose.
- [[Eval Leakage Policy]] — Explains how the test prompts were kept out of training, which is what makes these scores valid.
- [[Pac-Man Training Results]] — Gives the before-and-after scores of my Pac-Man agent, measured the same way on fixed evaluation games.

## Sources

- [[Custom LLM README#Results at a glance|Custom LLM README § Results at a glance]] · source S1 · lines 14–24
- [[Custom LLM README#4.1 Scores by group and category|Custom LLM README § 4.1 Scores by group and category]] · source S1 · lines 321–337

Original file: `vault/raw/Custom LLM README.md` (unchanged; SHA-256 `c8971e5d4ef04c14…`)
