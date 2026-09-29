---
title: Networking Tracker Deployment
folder: Projects
source_id: S2
source_file: raw/Networking Tracker README.md
source_sha256: 791a30402c37434d
source_sections:
  - "Production verification"
  - "Deployment"
generated_by: gemma4:e2b Q4_K_M (Ollama 0.20.7, local)
generated_at: 2026-09-29
reviewed: false
---

# Networking Tracker Deployment

This document details the production verification and deployment process for the Networking Tracker application. It outlines the steps for deploying the application and testing its security and functionality.

## Key details

- Deployment `dpl_…ado1a7ss5` serves `https://networking-tracker-gules.vercel.app`.
- The black-box lifecycle verification passed 16 tests, with 0 failures.
- Two-account privacy tests against production passed, with 1 test file passing.
- The deployment process involves pushing to GitHub and using `vercel login` and `vercel link`.
- Production environment variables are added via `vercel env add` commands.
- The public production domain registered is `networking-tracker-gules.vercel.app`.
- The deployment process requires adding the deployed domain to Neon Auth's trusted origins.

## Related notes

- [[Networking Tracker Overview]] — This note details the deployment and testing process for the Networking Tracker application.
- [[Networking Tracker Testing]] — This note describes the testing process for the Networking Tracker application.
- [[Networking Tracker Limitations]] — This note lists the known limitations of the Networking Tracker application.

## Sources

- [[Networking Tracker README#Production verification|Networking Tracker README § Production verification]] · source S2 · lines 349–390
- [[Networking Tracker README#Deployment|Networking Tracker README § Deployment]] · source S2 · lines 398–420

Original file: `vault/raw/Networking Tracker README.md` (unchanged; SHA-256 `791a30402c37434d…`)
