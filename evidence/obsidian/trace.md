**One note, traced to a related note and back to the original evidence.**

1. [`vault/index.md`](vault/index.md) lists **Negation Failure** under *Lessons*.
2. [`vault/wiki/Lessons/Negation Failure.md`](<vault/wiki/Lessons/Negation Failure.md>) says negation scored 1/3 and that the
   model chose `tea`, the negated word. Its *Related notes* link to **Custom LLM Eval Results** with the reason
   "Gives the scores by category, where negation is the only taught category at chance."
3. [`vault/wiki/Results/Custom LLM Eval Results.md`](<vault/wiki/Results/Custom LLM Eval Results.md>) gives 20 and 30 correct
   of 48 and links back. Its *Sources* point to `Custom LLM README § Results at a glance` and `§ 4.1`.
4. The first note's *Sources* link `Custom LLM README § 7. One limitation and my next experiment` opens the original at
   lines 519 to 528 of [`vault/raw/Custom LLM README.md`](<vault/raw/Custom LLM README.md>), where the sentence reads:
   "Negation transfer failed (1/3, chance) … it picked the *negated* word (`tea`)".

| The related note, reached by its link | The original passage, reached by the source reference |
|---|---|
| ![Related note](evidence/obsidian/4-related-note.png) | ![Original source passage](evidence/obsidian/5-original-source-passage.png) |

The same passage is what `ask` retrieved and cited for test 2, so the wiki a person browses and the evidence the model
answers from lead to the same lines.
