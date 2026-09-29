---
title: Sampling Temperature
folder: Concepts
source_id: S1
source_file: raw/Custom LLM README.md
source_sha256: c8971e5d4ef04c14
source_sections:
  - "3. Evidence from inside the network > 3.7 Temperature (inference only, weights unchanged)"
generated_by: gemma4:e2b Q4_K_M (Ollama 0.20.7, local)
generated_at: 2026-09-29
reviewed: true
reviewed_by: Brian Arevalo Ramos, with Claude (AI assistant)
reviewed_at: 2026-09-29
---

# Sampling Temperature

I experimented with three different temperatures for inference, keeping the model, start token, and seed the same. These temperatures resulted in different sampling behaviors.

## Key details

- I used three temperatures: 0.3, 0.8, and 1.2.
- Temperature divides the scores before the softmax.
- At T = 0.3, the distribution is sharpened toward the most likely word, and the four samples collapse onto the same starter template.
- At T = 1.2, the distribution is flattened and rarer continuations appear, including a broken one ("the take poor are opposites .").
- No weight changed between these samples, only the sampling rule.

## Related notes

- [[Custom LLM Training Evidence]] — Gives the next-word probabilities that temperature reshapes before a word is drawn.
- [[Custom LLM Chat Interface]] — Describes the chat interface, where every reply is sampled one word at a time.

## Sources

- [[Custom LLM README#3.7 Temperature (inference only, weights unchanged)|Custom LLM README § 3.7 Temperature (inference only, weights unchanged)]] · source S1 · lines 278–307

Original file: `vault/raw/Custom LLM README.md` (unchanged; SHA-256 `c8971e5d4ef04c14…`)
