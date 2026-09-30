# Evidence card: ask

- **Mode:** ask (standalone, no chat history) · **Execution:** local
- **Recorded:** 2026-09-29 17:29:53 PDT · **Network:** connected (Wi-Fi On, default route True, outside host answered True)
- **Model:** gemma4:e2b · 5.1B · Q4_K_M · digest 7fbdbf8f5e45 · Ollama 0.20.7
- **Model memory:** 7.68 GB loaded, 100% CPU

## Question

What name did I decide on for my next project?

## Retrieved passages

Query terms: `name, decide, next, project` · not in any source: `decide`

### [1] `vault/raw/Networking Tracker README.md` › Local setup (lines 133–163)
score 8.09 · matched: name, project · found via keyword

> ```bash
> git clone https://github.com/BuildingBrian/networking-tracker.git
> cd networking-tracker
> npm install
> ```
> 
> **1. Create the Neon project** — either in the [Neon Console](https://console.neon.tech) (create a project → enable **Auth** → enable **Data API**) or with the CLI:
> 
> ```bash
> npm i -g neon@latest && neon login
> neon neon-auth enable --project-id <id> --branch production
> neon data-api  create --project-id <id> --branch production --database neondb
> neon neon-auth domain allow-localhost enable --project-id <id> --branch production   # lets localhost sign in
> ```
> 
> **2. Configure the environment**
> 
> ```bash
> cp .env.example .env.local
> openssl rand -base64 32        # → NEON_AUTH_COOKIE_SECRET
> ```
> 
> Fill in `.env.local` with the Auth URL, Data API URL, and pooled connection string from Neon (`neon connection-string production --project-id <id> --database-name neondb --role-name neondb_owner --pooled`).
> 
> **3. Apply the schema and RLS policies**
> 
> ```bash
> npm run db:push
> ```
> 
> This runs `db/schema.sql` over Neon's HTTP driver and then prints the RLS flags, every policy with its `USING` / `WITH CHECK` expression, and every column — so the security requirements are verifiable from the terminal.

### [2] `vault/raw/Networking Tracker README.md` › Tests > Test output (lines 297–326)
score 4.73 · matched: name · found via keyword

> ```
>  ✓ tests/validation.test.ts > contact validation — name > rejects an empty name with a clear message
>  ✓ tests/validation.test.ts > contact validation — name > rejects a name that is only whitespace
>  ✓ tests/validation.test.ts > contact validation — name > rejects a missing name
>  ✓ tests/validation.test.ts > contact validation — name > rejects a name longer than 200 characters
>  ✓ tests/validation.test.ts > contact validation — name > trims surrounding whitespace from an otherwise valid name
>  ✓ tests/validation.test.ts > contact validation — priority > accepts the valid priority "high"
>  ✓ tests/validation.test.ts > contact validation — priority > accepts the valid priority "medium"
>  ✓ tests/validation.test.ts > contact validation — priority > accepts the valid priority "low"
>  ✓ tests/validation.test.ts > contact validation — priority > rejects a priority outside high / medium / low
> ```

### [3] `vault/raw/Networking Tracker README.md` › Deployment (lines 413–420)
score 4.38 · matched: project · found via keyword

>    `DATABASE_URL` is deliberately **not** added — the running app never uses it.
> 4. `vercel --prod`.
> 5. Add the deployed domain to Neon Auth's trusted origins so sign-in works there:
> 
>    ```bash
>    neon neon-auth domain add https://<your-app>.vercel.app --project-id <id> --branch production
>    ```
> 
>    For this deployment the public production domain `networking-tracker-gules.vercel.app` is registered. Vercel also generates a `<project>-<team>.vercel.app` alias, but Deployment Protection puts a Vercel login in front of it — so that one is deliberately *not* the URL in this README.
> 6. Open the public URL in a private window, create two accounts, and confirm neither can see the other's contacts. The same can be automated: `TEST_APP_URL=https://<your-app>.vercel.app npm test`.

### [4] `vault/raw/Networking Tracker README.md` › Tests > Test output (lines 295–295)
score 4.26 · matched: project · found via keyword

> `npm test` on 2026-09-08 against the live Neon project (`FORCE_COLOR=0 npx vitest run --reporter=verbose`, saved as [`docs/test-output.txt`](docs/test-output.txt)):

## Actual answer

**Status:** insufficient_evidence — the model found no answer in the passages

Insufficient evidence: the wiki sources do not contain this information.

Raw model reply before the harness applied its rules:

```
INSUFFICIENT EVIDENCE
```

## Citation check (done by the harness)

- Cited passages: [] · valid: [] · not retrieved: []
- Figures in the answer: []
- Figures missing from the cited passages: []

## Timing

29.01 s total · prompt 1223 tokens at 43.2 tokens/s · answer 6 tokens at 15.6 tokens/s

## My assessment

_to be written after reading the cited passages_
