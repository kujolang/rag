# Supply-Chain Security and SBOM

This project includes release-time and CI controls to improve software supply-chain visibility.

## What Is Generated

Release artifacts now include:

- `release-manifest.json`: deterministic file inventory with SHA-256 digests
- `SHA256SUMS.txt`: checksum manifest for artifact verification
- `sbom.cyclonedx.json`: CycloneDX SBOM generated from the release manifest
- `supply-chain-scan-release-gates.json`: dependency scan report for `.github/workflows/release-gates.yml`
- `supply-chain-scan-release-artifacts.json`: dependency scan report for `.github/workflows/release-artifacts.yml`
- `supply-chain-scan-env-surface.json`: secret-surface scan report for `.env.example`

## CI Enforcement

Two CI workflows enforce supply-chain controls:

- `.github/workflows/release-gates.yml`
  - Runs deterministic file-scoped scans and uploads all scan outputs as artifacts.
  - Fails when high severity findings are detected.
- `.github/workflows/release-artifacts.yml`
  - Verifies SBOM generation for tagged releases.
  - Runs deterministic file-scoped scans and stores outputs in the release artifact directory.
  - Blocks release artifact publication when high severity findings are detected.

## Scan Behavior

`scripts/run_supply_chain_scan.kujo` currently checks:

- High severity secret indicators (private key material and common token formats).
- Workflow action references that use floating branch refs (for example `@main`), which are treated as high severity.
- Unpinned workflow action references that are not commit-SHA pinned, reported as medium severity.
- Potential remote-script execution patterns (`curl | bash` or `curl | sh`) as high severity.

A non-zero exit is returned when any high severity findings are present.

## Local Usage

Run a local scan:

```bash
kujo run scripts/run_supply_chain_scan.kujo --interpreter --root .github/workflows/release-gates.yml --output ./results/supply-chain-scan-release-gates.json
kujo run scripts/run_supply_chain_scan.kujo --interpreter --root .github/workflows/release-artifacts.yml --output ./results/supply-chain-scan-release-artifacts.json
kujo run scripts/run_supply_chain_scan.kujo --interpreter --root .env.example --output ./results/supply-chain-scan-env-surface.json
```

Generate release artifacts (includes SBOM):

```bash
kujo run scripts/build_release_artifacts.kujo --interpreter --version vX.Y.Z --notes ./docs/releases/vX.Y.Z.md --output-dir ./results/releases
```
