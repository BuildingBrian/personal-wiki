---
title: Networking Tracker Limitations
folder: Lessons
source_id: S2
source_file: raw/Networking Tracker README.md
source_sha256: 791a30402c37434d
source_sections:
  - "Known limitations and what I'd improve next"
generated_by: gemma4:e2b Q4_K_M (Ollama 0.20.7, local)
generated_at: 2026-09-29
reviewed: true
reviewed_by: Brian Arevalo Ramos, with Claude (AI assistant)
reviewed_at: 2026-09-29
---

# Networking Tracker Limitations

I have identified several known limitations in my Networking Tracker. These limitations relate to email verification, data management, UI interactions, search capabilities, and testing coverage.

## Key details

- Email verification is off, and sign-up accepts any syntactically valid address.
- Test runs leave throwaway accounts behind, as each RLS and screenshot run creates fresh `@example.com` users.
- Delete uses `window.confirm`, which is accessible but I would use a shadcn `AlertDialog`.
- Search is a `LIKE` scan, which would require a `pg_trgm` index if the network grew large.
- There is no pagination, and cursor pagination on `(created_at, id)` is the natural next step.
- `@neondatabase/neon-js` is a beta SDK (0.7.0-beta), and its `getAccessToken` helper 404s against Managed Better Auth today.
- There is no optimistic UI, as every mutation refetches the list.
- Tests cover validation and RLS, but not the UI; Playwright tests for sign-in → add → edit → delete would be the highest-value addition.

## Related notes

- [[Networking Tracker Testing]] — Gives what is tested today: 25 tests covering validation and privacy, and 16 checks against the live app.
- [[Networking Tracker Architecture]] — Describes the Next.js, database, and authentication technologies used in the tracker's design.

## Sources

- [[Networking Tracker README#Known limitations and what I'd improve next|Networking Tracker README § Known limitations and what I'd improve next]] · source S2 · lines 426–433

Original file: `vault/raw/Networking Tracker README.md` (unchanged; SHA-256 `791a30402c37434d…`)
