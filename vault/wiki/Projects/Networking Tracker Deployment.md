---
title: Networking Tracker Deployment
folder: Projects
source_id: S2
source_file: raw/Networking Tracker README.md
source_sha256: 791a30402c37434d
source_sections:
  - "Deployment"
  - "Environment variables"
generated_by: gemma4:e2b Q4_K_M (Ollama 0.20.7, local)
generated_at: 2026-09-29
reviewed: true
reviewed_by: Brian Arevalo Ramos, with Claude (AI assistant)
reviewed_at: 2026-09-29
---

# Networking Tracker Deployment

I outline the steps I take to deploy the Networking Tracker. This process involves pushing to GitHub, using Vercel, setting environment variables, and configuring domain trust.

## Key details

- I push the repository to GitHub.
- I use `vercel login` and then `vercel link` from the repo root.
- I add production environment variables via the Vercel settings or using specific commands.
- I use commands to add `NEXT_PUBLIC_NEON_AUTH_URL` and `NEXT_PUBLIC_NEON_DATA_API_URL` as public.
- I use `printf` to add `NEON_AUTH_BASE_URL` and `NEON_AUTH_COOKIE_SECRET` as sensitive.
- I run `vercel --prod` to deploy.
- I add the public production domain `networking-tracker-gules.vercel.app` to Neon Auth's trusted origins.
- I can automate testing by setting `TEST_APP_URL=https://<your-app>.vercel.app` and running `npm test`.

## Related notes

- [[Networking Tracker Architecture]] — Describes the stack being deployed: Next.js on Vercel with Neon Postgres and Neon Auth.
- [[Networking Tracker Testing]] — Shows testing details including input validation and two-account privacy proofs for the deployed application.

## Sources

- [[Networking Tracker README#Deployment|Networking Tracker README § Deployment]] · source S2 · lines 398–420
- [[Networking Tracker README#Environment variables|Networking Tracker README § Environment variables]] · source S2 · lines 186–196

Original file: `vault/raw/Networking Tracker README.md` (unchanged; SHA-256 `791a30402c37434d…`)
