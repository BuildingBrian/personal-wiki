---
title: Networking Tracker Testing
folder: Projects
source_id: S2
source_file: raw/Networking Tracker README.md
source_sha256: 791a30402c37434d
source_sections:
  - "Tests"
  - "Tests > Test output"
  - "Grading evidence"
generated_by: gemma4:e2b Q4_K_M (Ollama 0.20.7, local)
generated_at: 2026-09-29
reviewed: false
---

# Networking Tracker Testing

The project has two test suites, totaling 25 tests, which are executed via `npm test`. One suite focuses on input validation, and the other tests row-level security (RLS) for two-account privacy.

## Key details

- There are two suites, totaling 25 tests.
- `tests/validation.test.ts` contains 18 tests and requires no credentials.
- `tests/rls.test.ts` contains 7 tests related to the two-account privacy proof.
- The RLS tests require a configured `.env.local` and the app running to execute successfully.
- The RLS tests involve signing up two throwaway accounts and testing access to public data via the Data API URL.
- Validation tests cover scenarios like empty names, whitespace-only names, missing names, and over-length names.
- The RLS tests verify that User A can read their own contact, but User B cannot `SELECT` User A's contact.
- The test output was generated on 2026-09-08 against the live Neon project.

## Related notes

- [[Networking Tracker Limitations]] — This note describes the testing process for the application.
- [[Networking Tracker Deployment]] — This document details the deployment and testing process for the application.
- [[Networking Tracker Overview]] — This note describes the core functionality and purpose of the application.

## Sources

- [[Networking Tracker README#Tests|Networking Tracker README § Tests]] · source S2 · lines 271–291
- [[Networking Tracker README#Test output|Networking Tracker README § Test output]] · source S2 · lines 295–326
- [[Networking Tracker README#Grading evidence|Networking Tracker README § Grading evidence]] · source S2 · lines 332–343

Original file: `vault/raw/Networking Tracker README.md` (unchanged; SHA-256 `791a30402c37434d…`)
