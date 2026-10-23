# RAG deployment discovery — 2026-10-22

## Confirmed running services

The launch agent `com.kujo.rag.docs` runs `scripts/run_local_docs_service.py`, loading private host configuration from `data/local-kujo-docs/service.json`. Its listener is **127.0.0.1:8787** on the maintainer's Mac. `/health` and `/ready` returned 200; health reported 184 chunks. Anonymous `/metrics` returned 401; a deliberately invalid bearer credential returned 403. No data-changing operations or denial-of-service probes were sent to this existing service.

The configured namespace is `kujo_docs`, authentication is bearer, RBAC is enabled with reader as the default role, and ingestion is confined to the local documentation corpus. Environment is `local`, strict mode is false, and neither auditing/fail-closed audit nor at-rest encryption is enabled in its configuration (the application defaults are false). This is a local documentation service, not evidence of a production-hardened hosted deployment. Listener inspection confirms loopback binding; it does not exclude an unknown external reverse proxy.

A second existing process listens on **127.0.0.1:18787** from the RAG checkout. Its health/readiness endpoints returned 200 and reported an empty index. Its operational purpose was not established. Both services were preserved without restart or configuration changes.

## Public hosting evidence

GitHub records a successful temporary `cloudflare-staging` workflow run **33895783365** from September 4. Its deployment **6268650588** was subsequently marked **inactive** at 16:40:03 UTC that day. The repository documentation describes this as temporary testing, not permanent production hosting. No downloadable artifacts were returned for that run in this discovery.

DNS lookups for `rag.kujolang.ai`, `rag-staging.kujolang.ai` and `knowledge.kujolang.ai` returned no address. No running cloudflared connector or local `.cloudflared` configuration was found. These checks do not rule out another hostname or remote hosting account.

The saved Wrangler OAuth credential was used only for a read-only Cloudflare zone query. Cloudflare returned HTTP 403, error **9109: Invalid access token**. No credential value was printed or committed. Consequently the current zone, DNS, Worker and tunnel inventory cannot yet be verified.

## Exact inputs required to continue

1. Refresh Cloudflare authentication on this Mac, or provide access through a signed-in hosting dashboard. Do not paste tokens into chat. This allows discovery of the actual DNS, tunnels, Access applications and hosting routes without guessing.
2. If the intended public service is hosted in a different account/provider, identify that account/provider or its hostname. If there is no hosted deployment, confirm whether the goal is a local-only tool release or a new hosted production deployment; these have different applicable operational requirements.
3. For a hosted deployment, identify the intended independent audit-storage destination and retention policy, plus who can approve security and operational access. An append-only file on this Mac cannot establish independent immutable retention.
4. After actual deployment checks, the accountable owner must reconcile the unverified historical critical finding/exception and approve the current threat model/readiness packet. The human incident exercise still needs real operational ownership and escalation decisions; completed automated drills already supply technical recovery evidence.

No production attestation or release approval is claimed. The previously recorded local/hosted test results remain valid for their stated source commits, not automatically for these long-running service processes.
