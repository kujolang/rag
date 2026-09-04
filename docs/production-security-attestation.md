# Production Security Attestation

This is the deployment gate for the two controls that cannot be proven from the
repository alone: the identity-aware reverse-proxy boundary (TM-02/TM-03) and
the independently protected audit sink (TM-11). A completed form is evidence,
not a place to store credentials.

## What can be completed before infrastructure exists

- Review `docs/security-reviews/TM-2026-08-RAG-draft.md` and assign the named
  Security and Operations reviewers.
- Select an ingress and audit-storage provider, define retention, and define
  the role-to-namespace mapping.
- Copy `config/production_security_attestation.template.json` to a private
  deployment repository. Do not commit a completed production attestation here
  if it identifies private hosts or internal topology.
- Create the evidence directory and pre-register the test cases below.
- Run the repository tests and the attestation validator against synthetic
  fixtures. These steps require no production service and no paid account.

The remaining checks require a real deployment because screenshots, config
exports, or test output from a hypothetical proxy or storage account are not
attestations.

## Required proxy evidence

Use a private origin. The production RAG listener must not have a publicly
routable ingress path. The identity-aware proxy must validate the JWT signature
against a fail-closed HTTPS JWKS source, restrict accepted algorithms, issuer,
audience, expiry and not-before values, remove every inbound `x-kujo-claim-*`,
`x-kujo-role`, `x-kujo-namespace`, and `x-kujo-proxy-secret` value, then rebuild
only verified claims. The proxy attestation secret belongs in a secret manager.

Capture sanitized command output for all of these checks:

1. An unauthenticated request is rejected at the edge.
2. A token with a bad signature, wrong issuer, wrong audience, expired time, or
   unsupported algorithm is rejected before the origin.
3. A valid low-privilege identity cannot become writer/admin or switch to an
   unauthorized namespace by supplying Kujo headers.
4. The same forged-header request sent directly to the origin is unreachable
   from an external network.
5. The RAG service accepts only the actual local/private proxy peer and rejects
   an incorrect proxy attestation secret.
6. TLS, origin connect, response-header, idle, and total request timeouts are no
   weaker than the application/runtime limits.
7. The deployed release commit and Kujo runtime version match the attestation.

For Cloudflare, the recommended topology is Cloudflare Access -> Cloudflare
Tunnel -> an origin-side JWT-validation/header-mapping adapter -> RAG bound to
loopback. Tunnel removes the need for a public origin listener, but it does not
replace application-token verification. Validate `Cf-Access-Jwt-Assertion`
against the team JWKS, issuer, and Access application audience in the adapter.
Map only an explicit allowlist of identity attributes to Kujo roles and
namespaces; never copy arbitrary JWT claims into header names.

## Required immutable-audit evidence

The application writes a keyed, locally verifiable append log. Production must
also export completed log segments and their checkpoint state to storage under
a different security boundary. The exporter credential may create objects but
must not overwrite or delete them. Retention-policy administration must use a
separate identity.

Capture sanitized evidence for:

1. The destination's immutable-retention rule and retention period.
2. Writer policy showing create-only/append-only access and no delete,
   overwrite, lifecycle, retention, or account-administration permission.
3. A separate retention administrator and documented break-glass procedure.
4. Encryption-at-rest and access-log settings.
5. Upload of a unique audit segment and state checkpoint, followed by download,
   SHA-256 comparison, and `verify_audit_chain` verification.
6. A denied overwrite and denied early-delete attempt for that object.
7. Exporter-failure monitoring and an alert-delivery test.
8. Recovery/readback ownership, rotation, retention expiry, and incident steps.

Cloudflare R2 bucket locks can prevent object deletion and overwriting for a
retention period. A lock alone is insufficient: the uploader token still needs
least privilege, administrative identities must be separate, and a readback
test must prove the uploaded bytes and local chain match.

## Evidence handling and validation

Store sanitized text/JSON artifacts under a protected evidence root such as
`evidence/production-security/<environment>/<date>/`. Do not store tokens,
cookies, shared secrets, private keys, raw sensitive document contents, or
unredacted identity data. Record each artifact path and `sha256_file` digest in
the attestation.

Run the gate with the signed Kujo runtime:

```bash
KUJO_RAG_PRODUCTION_ATTESTATION_PATH=/private/deployment/production-attestation.json \
KUJO_RAG_PRODUCTION_EVIDENCE_ROOT=/private/deployment/evidence/production-security \
KUJO_RAG_PRODUCTION_ATTESTATION_OUTPUT_PATH=./results/security/production-security-status.json \
KUJO_BIN=/absolute/path/to/kujo \
  /absolute/path/to/kujo run scripts/run_production_security_attestation_review.kujo --interpreter
```

The gate fails closed when controls, evidence digests, or approvals are
missing. It deliberately does not contact providers: an accountable reviewer
must first collect and sanitize the provider-side evidence.

## Approval and closeout

After the validator passes, the Security reviewer records TM-01 through TM-11
dispositions in the threat-model packet. The Operations reviewer confirms the
deployed commit, runtime, proxy, monitoring, retention, and recovery ownership.
Only then update `config/threat_model_review_plan.json` with the real review ID,
timestamp, and reviewer and rerun the complete release gate.
