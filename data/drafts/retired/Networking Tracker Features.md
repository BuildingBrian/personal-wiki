---
title: Networking Tracker Features
folder: Projects
source_id: S2
source_file: raw/Networking Tracker README.md
source_sha256: 791a30402c37434d
source_sections:
  - "Features"
generated_by: gemma4:e2b Q4_K_M (Ollama 0.20.7, local)
generated_at: 2026-09-29
reviewed: false
---

# Networking Tracker Features

The Networking Tracker features include secure authentication, a private contact list, detailed contact management, and robust sorting and filtering capabilities. It also provides clear user feedback and responsive design.

## Key details

- Email + password sign-up, sign-in, and sign-out are handled via Neon Managed Better Auth, with the session in an httpOnly signed cookie.
- There is a private contact list per account, showing only the user's own rows, enforced by the database and tests.
- Users can create, view, edit, and delete contacts with fields for name, company, role, where you met, notes, and priority.
- Priority is constrained to `high` / `medium` / `low` in the UI `<Select>`, the server-side Zod schema, and a Postgres `CHECK` constraint.
- Sorting options include date added, name, company, or priority, in ascending or descending order.
- Priority sorts in the order high → medium → low, not alphabetically.
- Filtering is available by priority and searching across name, company, role, and where you met.
- The system provides understandable loading, empty, success, and error states, including a distinct empty state for "no contacts yet" versus "no contacts match these filters", and a retry button for load failures.

## Related notes

- [[Networking Tracker Overview]] — Networking Tracker Overview describes the core functionality of the tracker.
- [[Networking Tracker Database]] — Networking Tracker Database details the data structure managed by the tracker.
- [[Networking Tracker Request Flow]] — Networking Tracker Request Flow outlines the process for managing contacts within the tracker.

## Sources

- [[Networking Tracker README#Features|Networking Tracker README § Features]] · source S2 · lines 54–62

Original file: `vault/raw/Networking Tracker README.md` (unchanged; SHA-256 `791a30402c37434d…`)
