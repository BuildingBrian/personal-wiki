---
title: Custom LLM Language Evals
folder: Results
source_id: S1
source_file: raw/Custom LLM README.md
source_sha256: c8971e5d4ef04c14
source_sections:
  - "4. The fixed 48-case language evals"
  - "4. The fixed 48-case language evals > 4.1 Scores by group and category"
  - "4. The fixed 48-case language evals > 4.2 All 48 cases"
  - "4. The fixed 48-case language evals > 4.3 Reading the results honestly"
  - "4. The fixed 48-case language evals > 4.4 How eval material stayed out of training"
  - "4. The fixed 48-case language evals > 4.5 Re-running the evals on the saved model"
  - "2. My runs"
generated_by: gemma4:e2b Q4_K_M (Ollama 0.20.7, local)
generated_at: 2026-09-29
reviewed: false
---

# Custom LLM Language Evals

The system uses fixed 48-case language evaluations where each case consists of a prompt, four single-word choices, and one answer. A case is scored as 1 if the correct word has the highest probability, with ties scoring 0, and unscorable cases count as 0 in "all-case success".

## Key details

- Each case is a prompt, four single-word choices, and one answer.
- The runner sends only the prompt to the model to read the probability for each of the four choice words.
- A case is unscorable if the prompt or answer contains a word outside the model's vocabulary.
- The runner also samples a free continuation, which is saved but not scored.
- The 16 `starter_patterns` prompts were withheld from the classroom sentences before splitting or building the vocabulary.
- The results include data for Experiment 1 untrained, Experiment 1 trained, Experiment 2 untrained, and Experiment 2 trained.
- The results are available in files such as `eval_results.csv` for different training stages.

## Related notes

- [[Custom LLM Evidence From Network]] — This note describes the scoring mechanism for language evaluations.
- [[Custom LLM Lessons Learned]] — This note details the observations and measurements from a Custom LLM.
- [[Building Custom LLM With NanoGPT]] — This note describes the learning process and generalization capabilities of the custom LLM.

## Sources

- [[Custom LLM README#4. The fixed 48-case language evals|Custom LLM README § 4. The fixed 48-case language evals]] · source S1 · lines 311–317
- [[Custom LLM README#4.1 Scores by group and category|Custom LLM README § 4.1 Scores by group and category]] · source S1 · lines 321–337
- [[Custom LLM README#4.2 All 48 cases|Custom LLM README § 4.2 All 48 cases]] · source S1 · lines 341–395
- [[Custom LLM README#4.3 Reading the results honestly|Custom LLM README § 4.3 Reading the results honestly]] · source S1 · lines 399–424
- [[Custom LLM README#4.4 How eval material stayed out of training|Custom LLM README § 4.4 How eval material stayed out of training]] · source S1 · lines 428–438
- [[Custom LLM README#4.5 Re-running the evals on the saved model|Custom LLM README § 4.5 Re-running the evals on the saved model]] · source S1 · lines 442–447
- [[Custom LLM README#2. My runs|Custom LLM README § 2. My runs]] · source S1 · lines 97–116

Original file: `vault/raw/Custom LLM README.md` (unchanged; SHA-256 `c8971e5d4ef04c14…`)
