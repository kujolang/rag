# RAG automated local recovery exercises — 2026-10-22

Operator: Codex, authorized by the repository owner. Environment: disposable macOS checkout, pinned Kujo v1.2.3, synthetic documents and credentials, loopback network only. No human incident commander, Security Team, SRE team or production environment participated. This is technical exercise evidence, not a completed human tabletop or production RTO/RPO approval.

| Scenario | Executed exercise | Result |
| --- | --- | --- |
| Authentication compromise | Replayed a revoked credential against 12 privileged routes in both token slots; queried with its replacement | Replays rejected; replacement worked |
| Data corruption | Backed up an ingested sentinel document and configuration, corrupted current state, restored, checked identical index bytes and query answer | Passed; measured local restore/query recovery 2.299 seconds; not a production RTO claim |
| Backup compromise | Tampered with the backup, attempted restore, checked target bytes | Rejected without changing target |
| Service degradation | Forced readiness failure, verified live=200/ready=503, restarted normally | Recovered live=200/ready=200 |
| Quality regression | Replaced the evaluation corpus with unrelated text, ran unchanged gates, restored the original corpus | Confidence/quality gates failed on corruption and recovered after rollback |

The quality baseline and restored corpus passed every quality gate, but both exceeded average/p95 latency limits on this busy machine. No performance threshold was changed. `recovery-drills.json` retains those failing release-gate results explicitly. A successful quality exercise does not mean release-performance approval. Hosted run 39882463502 at fix commit 79cacd2 subsequently passed all 73 aggregate tests and the standalone evaluation, canary, AI drift, multilingual and chunking gates, including their unchanged latency limits. Later large-corpus and performance/cost steps were skipped after the threat-model cadence failure; those remain required.

Reproduce in a disposable checkout:

```sh
KUJO_BIN=/absolute/path/to/kujo python3 scripts/run_local_security_exercises.py
KUJO_BIN=/absolute/path/to/kujo python3 scripts/run_local_recovery_drills.py
```

Scripts terminate their own listeners and remove generated credentials, temporary corpora and backups. They do not operate on production services. The full suite separately covers privacy workflows, audit tamper detection, ingest confinement and runtime HTTP defenses; consult its evidence summary for actual results.

## Still required for production readiness

1. Identify the real deployment and release source/runtime. Neither guessed RAG hostname currently resolves; do not assume local loopback services are publicly deployed.
2. Execute deployed proxy/JWT/header/role/isolation checks and independently protected immutable-audit upload/readback/overwrite/delete/retention/alert checks, with real evidence and accountable security/operations approval.
3. Conduct the human incident tabletop: actual incident/backup commanders, escalation and communication decisions, production rollback/restore ownership, lessons and owned follow-ups. These automated technical drills supply inputs; they cannot impersonate participants.
4. Reconcile unverified historical penetration findings and expired exception with current evidence; complete accountable threat-model and readiness review for candidate 1.1.0.
5. Pass unchanged performance and all applicable release gates on the final commit before release. No tag or release was created by these exercises.
