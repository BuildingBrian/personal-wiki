# Evidence card: test-3

- **Mode:** ask (standalone, no chat history) · **Execution:** local
- **Recorded:** 2026-09-29 16:40:08 PDT · **Network:** connected (Wi-Fi On, default route True, outside host answered False)
- **Model:** gemma4:e2b · 5.1B · Q4_K_M · digest 7fbdbf8f5e45 · Ollama 0.20.7
- **Model memory:** 7.68 GB loaded, 100% CPU

## Question

How does the networking tracker stop one user from reading another user's contacts?

## Expected (written before the harness existed)

- Kind: answerable — Third source, known supporting evidence in more than one section.
- Expected source: `vault/raw/Networking Tracker README.md` › Authentication and RLS ownership
- Expected answer: Row Level Security inside Postgres: a row is reachable only when auth.user_id() = user_id, enforced by the database rather than application code.

## Retrieved passages

Query terms: `network, tracker, stop, user, read, another, contact`

### [1] `vault/raw/Networking Tracker README.md` › Production verification (lines 376–388)
score 17.57 · matched: network, tracker, user, read, another, contact

> **Two-account privacy test against production — `TEST_APP_URL=https://networking-tracker-gules.vercel.app npx vitest run tests/rls.test.ts`** (accounts created through the live app's auth proxy; every assertion sent straight to the public Data API with each user's JWT):
> 
> ```
>  ✓ tests/rls.test.ts > RLS: one user cannot reach another user's contacts > User A can read their own contact 1354ms
>  ✓ tests/rls.test.ts > RLS: one user cannot reach another user's contacts > User B cannot SELECT User A's contact, even by its exact ID 374ms
>  ✓ tests/rls.test.ts > RLS: one user cannot reach another user's contacts > User B does not see User A's contact in an unfiltered list 380ms
>  ✓ tests/rls.test.ts > RLS: one user cannot reach another user's contacts > User B cannot UPDATE User A's contact 749ms
>  ✓ tests/rls.test.ts > RLS: one user cannot reach another user's contacts > User B cannot DELETE User A's contact 740ms
>  ✓ tests/rls.test.ts > RLS: one user cannot reach another user's contacts > User B cannot INSERT a row owned by User A 761ms
>  ✓ tests/rls.test.ts > RLS: one user cannot reach another user's contacts > User A cannot hand their own row to User B via UPDATE 1884ms
>  Test Files  1 passed (1)
>       Tests  7 passed (7)
> ```

### [2] `vault/raw/Networking Tracker README.md` › Tests > Test output (lines 297–326)
score 15.04 · matched: user, read, another, contact

> ```
>  ✓ tests/rls.test.ts > RLS: one user cannot reach another user's contacts > User A can read their own contact
>  ✓ tests/rls.test.ts > RLS: one user cannot reach another user's contacts > User B cannot SELECT User A's contact, even by its exact ID
>  ✓ tests/rls.test.ts > RLS: one user cannot reach another user's contacts > User B does not see User A's contact in an unfiltered list
>  ✓ tests/rls.test.ts > RLS: one user cannot reach another user's contacts > User B cannot UPDATE User A's contact
>  ✓ tests/rls.test.ts > RLS: one user cannot reach another user's contacts > User B cannot DELETE User A's contact
>  ✓ tests/rls.test.ts > RLS: one user cannot reach another user's contacts > User B cannot INSERT a row owned by User A
>  ✓ tests/rls.test.ts > RLS: one user cannot reach another user's contacts > User A cannot hand their own row to User B via UPDATE
> ```

### [3] `vault/raw/Networking Tracker README.md` › Networking Tracker (lines 3–7)
score 12.97 · matched: network, tracker, user, contact

> A private, per-user networking tracker for the people you want to stay connected with at Berkeley. Sign up, add the people you meet — name, company, role, where you met, notes, and a priority — then sort, filter, edit, and delete them. Every contact belongs to exactly one account, and that ownership is enforced by **Row Level Security inside Postgres** rather than by application code, so the data stays private even against a request made directly to the public Data API with a valid login.
> 
> **Live app:** **https://networking-tracker-gules.vercel.app**
> 
> **Repository:** https://github.com/BuildingBrian/networking-tracker

### [4] `vault/raw/Networking Tracker README.md` › Production verification (lines 349–374)
score 11.77 · matched: network, tracker, user, contact

> Everything above was re-run against the deployed app, not just locally. Deployment `dpl_…ado1a7ss5` (built 2026-09-08 22:31 PDT from stored Vercel environment variables, nothing passed inline) is what `https://networking-tracker-gules.vercel.app` serves.
> 
> **Black-box lifecycle — `BASE_URL=https://networking-tracker-gules.vercel.app npm run verify`:**
> 
> ```
> Verifying https://networking-tracker-gules.vercel.app
> 
> ✓ sign-in page renders  (HTTP 200)
> ✓ GET /api/contacts without a session → 401  (HTTP 401)
> ✓ /contacts without a session redirects to sign-in  (HTTP 307 → /auth/sign-in)
> ✓ sign-up succeeds and sets a session cookie  (HTTP 200, cookies: 2)
> ✓ new account starts with an empty list  (HTTP 200, 0 contacts)
> ✓ blank name + invalid priority → 400 with per-field errors  (HTTP 400: Name is required.)
> ✓ create → 201 with user_id stamped by the database  (HTTP 201, id f499ce1d-7168-4c3e-a1bc-549f603c6e2c)
> ✓ created contact appears in the list  (1 contacts)
> ✓ edit → 200 and the change is applied  (HTTP 200)
> ✓ attempt to reassign user_id is ignored; row stays owned by caller  (user_id unchanged)
> ✓ priority filter works (low → 1, high → 0)  (low 1, high 0)
> ✓ delete → 200  (HTTP 200)
> ✓ deleting it again → 404  (HTTP 404)
> ✓ list is empty again  (0 contacts)
> ✓ sign-out → 200  (HTTP 200)
> ✓ API refuses the request after sign-out → 401  (HTTP 401)
> 
> 16 passed, 0 failed
> ```

## Actual answer

**Status:** answered

Row Level Security inside Postgres enforces that every contact belongs to exactly one account, which keeps the data private even when a request is made directly to the public Data API with a valid login [3]. This mechanism prevents one user from reading another user's contacts [1, 2].

## Citation check (done by the harness)

- Cited passages: [1, 2, 3] · valid: [1, 2, 3] · not retrieved: []
- Figures in the answer: []
- Figures missing from the cited passages: []

## Timing

48.77 s total · prompt 1698 tokens at 39.7 tokens/s · answer 58 tokens at 10.5 tokens/s

## Automatic checks

- Expected passage retrieved at rank: NOT RETRIEVED

## My assessment

_to be written after reading the cited passages_
