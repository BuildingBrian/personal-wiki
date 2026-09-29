---
title: Row Level Security
folder: Concepts
source_id: S2
source_file: raw/Networking Tracker README.md
source_sha256: 791a30402c37434d
source_sections:
  - "Authentication and RLS ownership"
  - "Database schema"
generated_by: gemma4:e2b Q4_K_M (Ollama 0.20.7, local)
generated_at: 2026-09-29
reviewed: true
reviewed_by: Brian Arevalo Ramos, with Claude (AI assistant)
reviewed_at: 2026-09-29
---

# Row Level Security

I implement Row Level Security (RLS) on the `contacts` table to control row access based on user authentication. This is achieved by basing ownership rules on the `user_id` column, which is determined by the JWT issued during sign-in.

## Key details

- RLS is enabled and forced on `contacts`.
- I have four separate policies defined for `contacts`: `contacts_select_own`, `contacts_insert_own`, `contacts_update_own`, and `contacts_delete_own`.
- A row is reachable only when `auth.user_id() = user_id`.
- I use both `USING` and `WITH CHECK` clauses for `UPDATE` policies to prevent ownership transfer.
- The `user_id` column defaults to `auth.user_id()` and is used by every RLS policy.
- Both indexes lead with `user_id`, because every query is scoped to one user.

## Related notes

- [[Networking Tracker Testing]] — Gives the seven two-account tests that prove one user cannot reach another user's rows.
- [[Networking Tracker Architecture]] — Describes the architecture using Next.js, Neon Postgres with RLS, and managed authentication for implementation.
- [[Networking Tracker Overview]] — Describes the app whose contact list these policies keep private.

## Sources

- [[Networking Tracker README#Authentication and RLS ownership|Networking Tracker README § Authentication and RLS ownership]] · source S2 · lines 224–265
- [[Networking Tracker README#Database schema|Networking Tracker README § Database schema]] · source S2 · lines 202–218

Original file: `vault/raw/Networking Tracker README.md` (unchanged; SHA-256 `791a30402c37434d…`)
