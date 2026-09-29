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
reviewed: false
---

# Networking Tracker Limitations

The Networking Tracker has several known limitations that could be improved. These limitations relate to email verification, data management, user interface elements, search functionality, and testing coverage.

## Key details

- Email verification is off, and sign-up accepts any syntactically valid address.
- Test runs leave throwaway accounts behind, as each RLS and screenshot run creates fresh `@example.com` users.
- The delete function uses `window.confirm` instead of a shadcn `AlertDialog`.
- Search is a `LIKE` scan, which would require a `pg_trgm` index if the network grew large.
- There is no pagination, and cursor pagination on `(created_at, id)` is suggested as the next step.
- The `@neondatabase/neon-js` SDK is a beta version (0.7.0-beta) and its `getAccessToken` helper may fail against Managed Better Auth.
- There is no optimistic UI, as every mutation refetches the list.
- Tests cover validation and RLS, but not the UI; Playwright tests for sign-in → add → edit → delete would be a high-value addition.

## Related notes

- [[Networking Tracker Overview]] — This note lists the areas where the Networking Tracker has limitations.

## Sources

- [[Networking Tracker README#Known limitations and what I'd improve next|Networking Tracker README § Known limitations and what I'd improve next]] · source S2 · lines 426–433

Original file: `vault/raw/Networking Tracker README.md` (unchanged; SHA-256 `791a30402c37434d…`)
