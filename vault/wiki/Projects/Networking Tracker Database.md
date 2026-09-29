---
title: Networking Tracker Database
folder: Projects
source_id: S2
source_file: raw/Networking Tracker README.md
source_sha256: 791a30402c37434d
source_sections:
  - "Database schema"
generated_by: gemma4:e2b Q4_K_M (Ollama 0.20.7, local)
generated_at: 2026-09-29
reviewed: false
---

# Networking Tracker Database

This document describes the database schema for the Networking Tracker. It details the structure of the `public.contacts` table.

## Key details

- The authoritative definition is in `db/schema.sql`.
- The table is named `public.contacts`.
- The `id` column is of type `uuid` and is the primary key with a default of `gen_random_uuid()`.
- The `user_id` column is of type `text` and is not null with a default of `auth.user_id()`.
- The `name` column is not null and has checks for length greater than 0 and less than or equal to 200.
- The `company` and `role` columns are nullable.
- Indexes exist on `(user_id, created_at desc)` and `(user_id, priority_rank)`.

## Related notes

- [[Networking Tracker Overview]] — This note describes the database schema for the Networking Tracker.
- [[Networking Tracker Architecture]] — This describes the overall architecture of the Networking Tracker, including how it interacts with the database.
- [[Networking Tracker Features]] — This details the features available within the Networking Tracker, which are managed by the database.

## Sources

- [[Networking Tracker README#Database schema|Networking Tracker README § Database schema]] · source S2 · lines 202–218

Original file: `vault/raw/Networking Tracker README.md` (unchanged; SHA-256 `791a30402c37434d…`)
