# Branch Protection and Required Checks Policy

This document defines required branch protection behavior for production promotion.

## Protected Branches

- main (required)

## Required Status Checks

The following checks must be configured as required for main:
- runtime-support-matrix
- supply-chain-scan
- release-gates

These check names correspond to jobs in `.github/workflows/release-gates.yml`.

## Merge Policy

- Require pull request before merge.
- Require all required checks to pass before merge.
- Require branch to be up to date before merge.
- Require linear history or merge strategy policy per repository governance preference.
- Restrict direct pushes to main for non-admin users.

## Temporary Degraded-CI Failsafe

If CI infrastructure is degraded:
- use emergency override only with maintainer approval
- record issue link and incident note in PR
- require follow-up PR to re-run and validate checks

## Dry-Run Validation Procedure

To validate branch protection behavior:

1. Open a test PR branch.
2. Intentionally break one required check (for example, force `scripts/run_release_evaluation.kujo` to fail).
3. Confirm merge is blocked in GitHub UI while check is failing.
4. Restore check behavior and confirm merge becomes allowed.

## Auditable Verification Procedure

Repository maintainers should verify settings periodically using GitHub UI or CLI and store evidence in release notes.

Suggested fields to capture during verification:
- protected branch name
- required status check names
- PR requirement enabled
- direct push restrictions
- verification date and reviewer
