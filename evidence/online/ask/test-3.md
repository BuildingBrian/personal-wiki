# Evidence card: test-3

- **Mode:** ask (standalone, no chat history) · **Execution:** local
- **Recorded:** 2026-09-29 17:27:49 PDT · **Network:** connected (Wi-Fi On, default route True, outside host answered True)
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
score 17.57 · matched: network, tracker, user, read, another, contact · found via keyword

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
score 15.04 · matched: user, read, another, contact · found via keyword

> ```
>  ✓ tests/rls.test.ts > RLS: one user cannot reach another user's contacts > User A can read their own contact
>  ✓ tests/rls.test.ts > RLS: one user cannot reach another user's contacts > User B cannot SELECT User A's contact, even by its exact ID
>  ✓ tests/rls.test.ts > RLS: one user cannot reach another user's contacts > User B does not see User A's contact in an unfiltered list
>  ✓ tests/rls.test.ts > RLS: one user cannot reach another user's contacts > User B cannot UPDATE User A's contact
>  ✓ tests/rls.test.ts > RLS: one user cannot reach another user's contacts > User B cannot DELETE User A's contact
>  ✓ tests/rls.test.ts > RLS: one user cannot reach another user's contacts > User B cannot INSERT a row owned by User A
>  ✓ tests/rls.test.ts > RLS: one user cannot reach another user's contacts > User A cannot hand their own row to User B via UPDATE
> ```

### [3] `vault/raw/Networking Tracker README.md` › Authentication and RLS ownership (lines 249–265)
score 10.85 · matched: user, read, another, contact · found via wiki note: Row Level Security

> **Why `UPDATE` needs both clauses.** `USING` decides which rows a statement may *target*; `WITH CHECK` decides what those rows may look like *afterwards*. With `USING` alone, a user could edit a row they own and reassign `user_id` to someone else on the way out — handing their row to another account. `WITH CHECK` rejects any result that would no longer belong to the caller. The `BEFORE UPDATE` trigger additionally pins `user_id` to its old value, so even a future policy mistake could not silently transfer ownership.
> 
> The `anonymous` role is granted nothing on this table, so an unauthenticated request to the public Data API cannot read a single row.
> 
> `npm run db:push` prints what is actually in the database. Against the live project it reports:
> 
> ```
> RLS enabled: true   forced: true
> 
> 4 policies on public.contacts:
>   DELETE contacts_delete_own   USING (auth.user_id() = user_id)
>   INSERT contacts_insert_own   WITH CHECK (auth.user_id() = user_id)
>   SELECT contacts_select_own   USING (auth.user_id() = user_id)
>   UPDATE contacts_update_own   USING (auth.user_id() = user_id)   WITH CHECK (auth.user_id() = user_id)
> 
> user_id   text   NOT NULL   default auth.user_id()
> ```

### [4] `vault/raw/Networking Tracker README.md` › Authentication and RLS ownership (lines 224–247)
score 7.69 · matched: user, contact · found via wiki note: Row Level Security

> When a user signs in, Neon Auth issues a JWT. Every Data API request carries that JWT, and Postgres exposes its subject as **`auth.user_id()`**. `contacts.user_id` defaults to that value, so the database — not the application — decides who owns a row.
> 
> RLS is **enabled and forced** on `contacts` (forced so it applies to the table owner too), with four separate policies:
> 
> ```sql
> create policy contacts_select_own on public.contacts
>   for select to authenticated
>   using (auth.user_id() = user_id);
> 
> create policy contacts_insert_own on public.contacts
>   for insert to authenticated
>   with check (auth.user_id() = user_id);
> 
> create policy contacts_update_own on public.contacts
>   for update to authenticated
>   using (auth.user_id() = user_id)
>   with check (auth.user_id() = user_id);
> 
> create policy contacts_delete_own on public.contacts
>   for delete to authenticated
>   using (auth.user_id() = user_id);
> ```
> 
> **The ownership rule in one sentence:** a row is reachable only when `auth.user_id() = user_id`.

## Actual answer

**Status:** answered

One user cannot reach another user's contacts because of Row Level Security (RLS) policies [4]. The ownership rule is that a row is reachable only when `auth.user_id() = user_id` [4]. This is enforced by policies such as `contacts_select_own` which uses the condition `auth.user_id() = user_id` for selecting contacts [4].

## Citation check (done by the harness)

- Cited passages: [4] · valid: [4] · not retrieved: []
- Figures in the answer: []
- Figures missing from the cited passages: []

## Timing

49.61 s total · prompt 1647 tokens at 38.4 tokens/s · answer 85 tokens at 13.4 tokens/s

## Automatic checks

- Passage containing all expected strings ['Row Level Security', 'auth.user_id()']: rank NOT RETRIEVED
- Passage from the expected section "Authentication and RLS ownership": rank [3, 4]

## My assessment

_to be written after reading the cited passages_
