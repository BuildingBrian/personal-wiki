---
title: Custom LLM Lessons Learned
folder: Lessons
source_id: S1
source_file: raw/Custom LLM README.md
source_sha256: c8971e5d4ef04c14
source_sections:
  - "6. What I learned"
  - "7. One limitation and my next experiment"
  - "8. Reproduce and inspect"
  - "9. Reflection and where I go from here"
generated_by: gemma4:e2b Q4_K_M (Ollama 0.20.7, local)
generated_at: 2026-09-29
reviewed: false
---

# Custom LLM Lessons Learned

The custom LLM learned to associate word relationships and template shapes rather than memorizing specific sentences or facts. The model demonstrated the ability to generalize relationships within its learned world, despite limitations in negation transfer and handling unknown words.

## Key details

- The corpus consists of 6,559 short passages: 4,592 template sentences about eight everyday domains plus 1,967 teaching sentences.
- The model can teach which words go together in which slots, but it cannot teach grammar, facts, or long-range reasoning.
- A token is a piece of text the tokenizer cut out, and its ID is an arbitrary integer label.
- The vector is the row of 64 floating-point numbers stored at that ID in the embedding table, and "embedding" is the name for that learned mapping from ID to vector.
- Before training, the row was noise (-0.0576, -0.0048, …); after training it sits 0.97 cosine from `shopper` and `client`.
- The model is layers of matrix multiplications with non-linearities between them, and all 111,872 numbers in those matrices are adjustable.
- Loss is the negative log probability the model gave the true next word, averaged over a batch.
- Negation transfer failed with a 1/3 chance.

## Related notes

- [[Custom LLM Evidence From Network]] — This note summarizes the general learning outcome of the custom LLM.

## Sources

- [[Custom LLM README#6. What I learned|Custom LLM README § 6. What I learned]] · source S1 · lines 490–515
- [[Custom LLM README#7. One limitation and my next experiment|Custom LLM README § 7. One limitation and my next experiment]] · source S1 · lines 519–528
- [[Custom LLM README#8. Reproduce and inspect|Custom LLM README § 8. Reproduce and inspect]] · source S1 · lines 532–544
- [[Custom LLM README#9. Reflection and where I go from here|Custom LLM README § 9. Reflection and where I go from here]] · source S1 · lines 548–570

Original file: `vault/raw/Custom LLM README.md` (unchanged; SHA-256 `c8971e5d4ef04c14…`)
