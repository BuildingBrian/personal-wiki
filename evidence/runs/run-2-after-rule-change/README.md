# Run 2: after the first rule change (2026-09-29, 10:45)

Produced by the full demonstration script while online. Kept as it happened.

| Test | Status | Expected passage retrieved at rank | What happened |
|---|---|---|---|
| test-1 | answered | 1 and 2 | Correct numbers, but written as "[1] … [1]. [2] … [2].": the model started each sentence with a passage number and said the same fact twice. |
| test-2 | answered | 3 | **Fixed.** "Negation transfer failed [3]. The model chose the negated word, "tea" …" |
| test-3 | answered | not in the top 4 | Correct, citing the introduction and two test-output passages. |
| test-4 | insufficient evidence | n/a | Correct refusal. |

## What I changed after this run

Only the form of the answer. Rule 7 of the research rules now asks for one plain paragraph and forbids starting a
sentence with a bracketed number. The model then answered test 1 in clean prose but copied the score table out of the
passage in front of it, even when told not to. A small model echoes what it has just read. So the harness now removes
table lines from the answer it shows (`ask.tidy`), and the untouched reply stays in the evidence record as
`raw_model_reply`.
