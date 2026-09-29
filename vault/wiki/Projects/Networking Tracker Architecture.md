---
title: Networking Tracker Architecture
folder: Projects
source_id: S2
source_file: raw/Networking Tracker README.md
source_sha256: 791a30402c37434d
source_sections:
  - "Architecture"
  - "Technology stack and why"
generated_by: gemma4:e2b Q4_K_M (Ollama 0.20.7, local)
generated_at: 2026-09-29
reviewed: false
---

# Networking Tracker Architecture

The architecture separates the frontend (React client components) from the backend (Next.js Route Handlers) which interact with the database. Authentication relies on Neon Managed Better Auth to establish a user's identity via a session cookie and a JWT.

## Key details

- The Browser consists of React client components in `src/components/*`.
- Frontend components only talk to the app's own `/api` routes and never see database credentials.
- Backend logic resides in `src/app/api/contacts/route.ts` and `src/app/api/contacts/[id]/route.ts`.
- Handlers perform session authentication, Zod validation, and issue a Data API query.
- The session is stored in an `httpOnly, signed cookie` via `src/app/api/auth/[...path]/route.ts`.
- Database ownership is enforced by Row Level Security (RLS) policies defined in `db/schema.sql`.
- Validation exists in the server using Zod and in the database via `CHECK` constraints.
- Hosting is on Vercel, where server-only variables are environment variables.

## Related notes

- [[Networking Tracker Overview]] — Networking Tracker Overview describes the application's purpose.
- [[Networking Tracker Database]] — Networking Tracker Database describes the data structure the backend interacts with.
- [[Networking Tracker Deployment]] — Networking Tracker Deployment details how the application is set up and run.

## Sources

- [[Networking Tracker README#Architecture|Networking Tracker README § Architecture]] · source S2 · lines 83–112
- [[Networking Tracker README#Technology stack and why|Networking Tracker README § Technology stack and why]] · source S2 · lines 68–77

Original file: `vault/raw/Networking Tracker README.md` (unchanged; SHA-256 `791a30402c37434d…`)
