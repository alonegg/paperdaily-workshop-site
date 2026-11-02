# Initial validation

2026-11-02: allowlisted export 43 files, 57 audience slides, 49 built static files. Internal presenter notes removed. Every built local link resolves. Both ZIP bodies match their classroom manifest. Credential/private-path scan passed. Export tests passed: credential refusal, hash mismatch preserving existing export, ZIP traversal refusal before replacement. Current npm audit reports 0 vulnerabilities after updating pinned Wrangler from 4.83.0 to 4.156.1.

An initial local commit command continued after whitespace diagnostics on the upstream font-license CRLF file. The importer now normalizes published text newlines, retains original wording, re-exports and regenerates hashes. Source ZIP bytes remain exact. This fix is committed separately before first public push. No source font archive, historical materials or credential value is published.

Cloudflare read-only preflight: paperdaily.org zone active in selected account; no pre-existing workshop DNS record/domain. Scoped deploy token and a target-only SSH deploy key configured, private key file deleted. Public HTTPS, actual domain binding, CI execution and source-push propagation are still pending and will be recorded separately.
