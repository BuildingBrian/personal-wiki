---
title: Networking Tracker Overview
folder: Projects
source_id: S2
source_file: raw/Networking Tracker README.md
source_sha256: 791a30402c37434d
source_sections:
  - "Networking Tracker"
generated_by: gemma4:e2b Q4_K_M (Ollama 0.20.7, local)
generated_at: 2026-09-29
reviewed: false
---

# Networking Tracker Overview

The Networking Tracker is a private, per-user networking tracker for people at Berkeley. It allows users to sign up, add contacts with details, and manage them through sorting, filtering, editing, and deleting.

## Key details

- It is a private, per-user networking tracker for people you want to stay connected with at Berkeley.
- Users can add people with name, company, role, where you met, notes, and a priority.
- Every contact belongs to exactly one account.
- Ownership is enforced by Row Level Security inside Postgres rather than by application code.
- Data stays private even against a request made directly to the public Data API with a valid login.
- The live application is available at https://networking-tracker-gules.vercel.app.
- The repository is located at https://github.com/BuildingBrian/networking-tracker.

## Related notes

- [[Networking Tracker Deployment]] — Networking Tracker Deployment details the production verification and deployment process.
- [[Networking Tracker Features]] — Networking Tracker Features describes the application's functionalities.
- [[Networking Tracker Database]] — Networking Tracker Database describes the database structure for the tracker.

## Sources

- [[Networking Tracker README#Networking Tracker|Networking Tracker README § Networking Tracker]] · source S2 · lines 3–7

Original file: `vault/raw/Networking Tracker README.md` (unchanged; SHA-256 `791a30402c37434d…`)
