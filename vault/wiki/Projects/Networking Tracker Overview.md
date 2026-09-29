---
title: Networking Tracker Overview
folder: Projects
source_id: S2
source_file: raw/Networking Tracker README.md
source_sha256: 791a30402c37434d
source_sections:
  - "Networking Tracker"
  - "Features"
generated_by: gemma4:e2b Q4_K_M (Ollama 0.20.7, local)
generated_at: 2026-09-29
reviewed: true
reviewed_by: Brian Arevalo Ramos, with Claude (AI assistant)
reviewed_at: 2026-09-29
---

# Networking Tracker Overview

I have created a private, per-user networking tracker for people I want to stay connected with at Berkeley. I can sort, filter, edit, and delete my contacts within the application.

## Key details

- Every contact belongs to exactly one account, and this ownership is enforced by Row Level Security inside Postgres.
- I can create, view, edit, and delete contacts with fields for name, company, role, where I met, notes, and a priority.
- Priority is constrained to `high` / `medium` / `low` in the UI, the server-side Zod schema, and a Postgres `CHECK` constraint.
- I can sort by date added, name, company, or priority, in ascending or descending order.
- I can filter by priority and search across name, company, role, and where I met.
- I have understandable loading, empty, success, and error states, including a distinct empty state for "no contacts yet" versus "no contacts match these filters".
- My data survives refresh because it lives in Neon Postgres.

## Related notes

- [[Row Level Security]] — Explains how the database itself enforces that each contact belongs to one account.
- [[Networking Tracker Architecture]] — Describes the technology stack and architecture used to build the networking tracker application.
- [[Networking Tracker Limitations]] — Lists what the app does not do yet, such as email verification and pagination.

## Sources

- [[Networking Tracker README#Networking Tracker|Networking Tracker README § Networking Tracker]] · source S2 · lines 3–7
- [[Networking Tracker README#Features|Networking Tracker README § Features]] · source S2 · lines 54–62

Original file: `vault/raw/Networking Tracker README.md` (unchanged; SHA-256 `791a30402c37434d…`)
