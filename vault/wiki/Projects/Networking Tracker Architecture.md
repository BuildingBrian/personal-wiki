---
title: Networking Tracker Architecture
folder: Projects
source_id: S2
source_file: raw/Networking Tracker README.md
source_sha256: 791a30402c37434d
source_sections:
  - "Technology stack and why"
  - "Architecture"
  - "Request flow"
generated_by: gemma4:e2b Q4_K_M (Ollama 0.20.7, local)
generated_at: 2026-09-29
reviewed: true
reviewed_by: Brian Arevalo Ramos, with Claude (AI assistant)
reviewed_at: 2026-09-29
---

# Networking Tracker Architecture

I designed a networking tracker using a Next.js stack to keep the frontend and backend in one repository. I utilized Neon Postgres with Row Level Security for database-level ownership and Neon Managed Better Auth for JWT handling.

## Key details

- I chose Next.js 16 (App Router) and TypeScript for the framework.
- I used Tailwind CSS v4 and shadcn/ui for styling.
- I selected Neon Postgres as the database, which supports Row Level Security.
- Neon Managed Better Auth issues a JWT whose subject Postgres reads as `auth.user_id()`.
- I use Neon Data API (PostgREST) via `@neondatabase/neon-js` for data access.
- I use Zod for validation, sharing a schema between API routes and tests.
- The frontend consists of React client components in `src/components/*`.
- The backend is in `src/app/api/contacts/` and related routes.

## Related notes

- [[Row Level Security]] — Explains the ownership rule that this architecture pushes into the database instead of the application.
- [[Networking Tracker Deployment]] — Shows the deployment steps required to make the networking tracker live on the web.
- [[Networking Tracker Limitations]] — Lists known limitations regarding email verification, data management, UI interactions, search, and testing coverage.

## Sources

- [[Networking Tracker README#Technology stack and why|Networking Tracker README § Technology stack and why]] · source S2 · lines 68–77
- [[Networking Tracker README#Architecture|Networking Tracker README § Architecture]] · source S2 · lines 83–112
- [[Networking Tracker README#Request flow|Networking Tracker README § Request flow]] · source S2 · lines 118–127

Original file: `vault/raw/Networking Tracker README.md` (unchanged; SHA-256 `791a30402c37434d…`)
