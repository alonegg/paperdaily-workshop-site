# Public workshop site

Confirmed domain workshop.paperdaily.org; public dedicated repo alonegg/paperdaily-workshop-site. Source private repo alonegg/paperdaily-research-workshop/main. User explicitly authorized website, domain, repo publication and automatic updates on 2026-11-02.

Explicit public allowlist: audience slides (presenter notes removed), referenced assets/fonts, current HTML poster, two verified classroom skill ZIPs, selected teaching guides. Never copy historical materials, private logs, credentials, databases, or untracked archives.

Source push → target-only SSH write deploy key → sanitized content commit in site repo → site Actions build/validate/deploy → Cloudflare static assets → HTTPS verification. Site code changes deploy independently. No broad GitHub PAT stored. CF token scoped to account Workers and this zone routes/read. Site contains preparation, downloads, current poster, lecture and reading guides.
