# PaperDaily Workshop

Public participant website at https://workshop.paperdaily.org.

## Content and automatic updates

The private preparation repository `alonegg/paperdaily-research-workshop` remains the editing source. Its main-branch push runs a scoped export into this site's `content/` folder using a write deploy key limited to this repository. This repo's push then runs GitHub Actions build, validation, Cloudflare deployment and public version/download verification.

Update `workshop/index.html` / referenced assets, `poster/index.html` / referenced assets, or `workshop/handouts/{paperdaily,paperdaily-deep-research}.zip` and its manifest in the preparation repository, commit and push main. Local edits alone do not publish. Classroom ZIP hash/version metadata must be updated together; installed skills elsewhere on a laptop are not automatically published. Site code and preparation-page changes are edited in this repository.

Source-to-site export refuses malformed ZIPs, manifest mismatch, symlinks and credential patterns. Presenter notes are omitted from public slides. Historical archives, private logs, machine credentials and untracked files are never copied. The public repository contains only this sanitized subset. Links to private production/verification archives are labeled as unpublished, not copied.

## Local build

```
python3 -m pip install -r requirements.txt
python3 scripts/import_workshop.py --source /path/to/paperdaily-research-workshop
npm ci
npm run build
```

`dist/` is a generated, ignored output directory. `content/manifest.json` records the source commit and exported hashes. Public `/version.json` records both source and site release commits and classroom package hashes.

## Deployment and credentials

GitHub repo secret `CLOUDFLARE_API_TOKEN` and variable `CLOUDFLARE_ACCOUNT_ID` configure deployment. The source repo stores `WORKSHOP_SITE_DEPLOY_KEY`, restricted to writing this target repository. No broad GitHub PAT or Cloudflare global key is stored in this public repository. Never commit private key files, .env or credentials.

Cloudflare Workers Static Assets serves the site, with a custom domain limited to workshop.paperdaily.org. Existing PaperDaily services are not changed. Each deployment verifies canonical HTTPS, release identity and full-body SHA256 of both downloadable packages. Manual recovery: run source sync workflow, or site's Deploy workflow. Failed source validation leaves the previous public release intact.

Activity: 2026-11-05 morning; speaker 陈春林. No venue or registration link has been supplied. School-email registration requires email verification and effective institutional qualification; 300 daily credits are subject to account entitlement. No participant API keys are collected by the site.
