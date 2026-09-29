# Run 1: the first time the four questions met the harness (2026-09-29, about 09:50)

Kept as it happened. Nothing here was rerun or edited.

| Test | Status | Expected passage retrieved at rank | What happened |
|---|---|---|---|
| test-1 | answered | 1 and 2 | Correct: 492.0 untrained, 608.0 trained. |
| test-2 | insufficient evidence | 3 | **Failure.** The passage that says "Negation transfer failed ... it picked the negated word (tea)" was retrieved at rank 3, and a second one at rank 2, but the model refused to answer. |
| test-3 | answered | not in the top 4 | Correct answer from a different passage of the same source (the introduction). The section I expected was not retrieved. The model wrote "[1, 2]" as one citation. |
| test-4 | insufficient evidence | n/a | Correct refusal. |

## Two harness bugs this run exposed (both mine, both fixed before run 2)

1. **The network flag was wrong.** Test 1 says the internet was reachable and tests 2 to 4 say it was not, yet the
   laptop was online the whole time. The harness decided by opening a connection to one outside host, and the per-app
   firewall on this Mac (LuLu) lets some of those probes through and blocks others. A flag that can say "offline"
   while online would make offline evidence worthless, so the harness now reads the operating system instead: Wi-Fi
   power, whether a default network route exists, and the probe. It reports offline only when there is no route and
   no probe succeeds.
2. **Model memory reads "None" in test 1.** The harness read memory before the model had loaded. It now reads it
   after the call.

A third fix: the citation check only understood `[1]`, so it treated the "1" and "2" in `[1, 2]` as unsupported
figures. It now accepts both forms.
