---
title: Custom LLM Evidence From Network
folder: Results
source_id: S1
source_file: raw/Custom LLM README.md
source_sha256: c8971e5d4ef04c14
source_sections:
  - "3. Evidence from inside the network > 3.1 Loss curves"
  - "3. Evidence from inside the network > 3.2 Samples: untrained → halfway → final (same generation settings every time)"
  - "3. Evidence from inside the network > 3.3 One word, from text to ID to 64-number vector"
  - "3. Evidence from inside the network > 3.4 One real gradient and weight update"
  - "3. Evidence from inside the network > 3.5 Next-token probabilities before and after (prefix the customer)"
  - "3. Evidence from inside the network > 3.6 Attention rows"
  - "3. Evidence from inside the network > 3.7 Temperature (inference only, weights unchanged)"
generated_by: gemma4:e2b Q4_K_M (Ollama 0.20.7, local)
generated_at: 2026-09-29
reviewed: false
---

# Custom LLM Evidence From Network

This document details various measurements and observations from a Custom LLM, including loss curves, sample generation, token-to-ID mapping, weight updates, next-token probabilities, attention patterns, and temperature effects. It provides specific data points derived from experiments involving training and inference.

## Key details

- Loss curves are based on fixed panels of 20 training and 20 validation documents.
- The notebook records loss at step 0, halfway, and the end, resulting in three points per curve.
- Experiment 1 loss at step 0 was 4.9263 for training and 4.9275 for validation.
- Experiment 2 loss at step 0 was 5.9482 for training and 5.9767 for validation.
- Samples are generated at steps 0, 1500, and 3000 for both Experiment 1 and Experiment 2.
- The tokenizer builds its vocabulary from training passages only.
- The one-word trace shows the token 'today' maps to ID 1, and the target ID is 121.
- The first weight update for `customer`'s embedding row at step 0 was -0.057602.

## Related notes

- [[Custom LLM Lessons Learned]] — This note details measurements and observations from the Custom LLM.
- [[Custom LLM Language Evals]] — This note describes the evaluation process for the Custom LLM.
- [[Building Custom LLM With NanoGPT]] — This note details the process of building the Custom LLM.

## Sources

- [[Custom LLM README#3.1 Loss curves|Custom LLM README § 3.1 Loss curves]] · source S1 · lines 122–139
- [[Custom LLM README#3.2 Samples: untrained → halfway → final (same generation settings every time)|Custom LLM README § 3.2 Samples: untrained → halfway → final (same generation settings every time)]] · source S1 · lines 143–190
- [[Custom LLM README#3.3 One word, from text to ID to 64-number vector|Custom LLM README § 3.3 One word, from text to ID to 64-number vector]] · source S1 · lines 194–235
- [[Custom LLM README#3.4 One real gradient and weight update|Custom LLM README § 3.4 One real gradient and weight update]] · source S1 · lines 239–249
- [[Custom LLM README#3.5 Next-token probabilities before and after (prefix the customer)|Custom LLM README § 3.5 Next-token probabilities before and after (prefix the customer)]] · source S1 · lines 253–261
- [[Custom LLM README#3.6 Attention rows|Custom LLM README § 3.6 Attention rows]] · source S1 · lines 265–274
- [[Custom LLM README#3.7 Temperature (inference only, weights unchanged)|Custom LLM README § 3.7 Temperature (inference only, weights unchanged)]] · source S1 · lines 278–307

Original file: `vault/raw/Custom LLM README.md` (unchanged; SHA-256 `c8971e5d4ef04c14…`)
