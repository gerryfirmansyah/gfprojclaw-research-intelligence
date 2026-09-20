# J16 Admin Authentication — Reverse Proxy v0

Decision accepted by HUMAN: use a portable reverse-proxy authentication boundary for J16, designed so it can later be replaced by OIDC/SSO or application RBAC.

## Required boundary
- Protect the Admin Copilot document and `/api/admin/*`; protecting only the HTML is insufficient.
- Keep Research Copilot/read-only scientific projections outside the Admin credential boundary unless separately decided.
- HTTPS is mandatory.
- Username/password material and password hashes are deployment secrets and must not enter Git.
- Authentication is operational authorization only; it grants no scientific authority.
- Existing actor/reason fields remain audit metadata and are not authentication credentials.

## Portable deployment shape
Preferred shape is a dedicated Admin HTTPS origin served by Caddy. The same authenticated origin serves the Admin static UI and proxies its Admin API path, avoiding cross-origin credential handling in browser JavaScript. Public Research Copilot remains independently deployable.

A replacement host must create fresh Admin credentials out-of-band, validate Caddy configuration, verify unauthenticated requests are rejected, verify authenticated Admin UI/API access, and record the result without logging credentials.

## Activation gate
Do not activate a credentialed production gate until a real HUMAN Admin credential has been provisioned out-of-band and the Admin origin/API routing has been smoke-tested. Never commit a default password or generated credential to the repository.
