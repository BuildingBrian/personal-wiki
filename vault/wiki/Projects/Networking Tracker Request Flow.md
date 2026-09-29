---
title: Networking Tracker Request Flow
folder: Projects
source_id: S2
source_file: raw/Networking Tracker README.md
source_sha256: 791a30402c37434d
source_sections:
  - "Request flow"
generated_by: gemma4:e2b Q4_K_M (Ollama 0.20.7, local)
generated_at: 2026-09-29
reviewed: false
---

# Networking Tracker Request Flow

This document outlines the end-to-end request flow for adding, reading, updating, and deleting contacts. The process involves specific steps for authentication, data insertion, and policy enforcement.

## Key details

- Adding a contact starts with the user submitting the dialog form, which POSTs JSON to `/api/contacts`.
- The handler calls `getSessionUser()`, and no session results in a `401` error.
- The body is parsed with `contactInputSchema`; a blank name or priority outside `high|medium|low` results in a `400` with `{ error, fieldErrors }`.
- The handler builds a Data API client whose `getToken` exchanges the request's session cookie for the user's Neon Auth JWT.
- The `insert()` operation is sent without a `user_id`, allowing Postgres to fill it from `DEFAULT auth.user_id()`.
- The `contacts_insert_own` policy's `WITH CHECK` confirms the new row belongs to the caller.
- Reading, updating, and deleting follow the same path.
- `PATCH /api/contacts/:id` filters on `id` alone, as the `contacts_update_own` policy restricts visible rows.

## Related notes

- [[Networking Tracker Overview]] — This note describes the overall request flow for managing contacts within the Networking Tracker.
- [[Networking Tracker Database]] — This document details the database structure for the contacts managed by the Networking Tracker.
- [[Networking Tracker Features]] — This document describes the features and capabilities of the Networking Tracker, including contact management.

## Sources

- [[Networking Tracker README#Request flow|Networking Tracker README § Request flow]] · source S2 · lines 118–127

Original file: `vault/raw/Networking Tracker README.md` (unchanged; SHA-256 `791a30402c37434d…`)
