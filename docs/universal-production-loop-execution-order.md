# Kujo RAG Universal Production Loop Execution Order

This file defines the canonical loop order for executing docs/universal-production-hardening-checklist.md.

Use this order with one loop per PR/commit unless blocked by an explicit dependency.

## Operating Rules

1. Execute exactly one loop item per implementation cycle.
2. Keep loop order unless a dependency explicitly forces a skip.
3. For each completed loop:
- update docs/universal-production-hardening-checklist.md
- update docs/universal-production-progress-log.md
- update README.md when behavior/config/API/operations change
4. Use commit message format:
- hardening(LNNN): implement UPR-XXX <short summary>

## Standard Validation Gate Per Loop

Run these unless the loop explicitly replaces or extends them:
- kujo run tests/test_unit.kujo --interpreter
- kujo run tests/test_integration.kujo --interpreter
- kujo run tests/test_release_evaluation.kujo --interpreter
- kujo run scripts/run_release_evaluation.kujo --interpreter
- kujo run scripts/run_tests.kujo --interpreter

When API changes are involved:
- kujo run main.kujo --interpreter serve --host 127.0.0.1 --port 8787
- curl -s http://127.0.0.1:8787/health
- curl -s -X POST http://127.0.0.1:8787/ingest -H "Content-Type: application/json" -d '{"path":"./examples/kujo_docs","recursive":true}'
- curl -s -X POST http://127.0.0.1:8787/query -H "Content-Type: application/json" -d '{"query":"What is Kujo optimized for?"}'

## Canonical Loop Order (L001-L064)

### Wave A: Universal Blockers

1. L001 -> UPR-001 Publish Kujo runtime support matrix and de-risk interpreter dependence
2. L002 -> UPR-002 Require native-mode parity for core ingest/query flows
3. L003 -> UPR-003 Enforce branch protection and required gate checks
4. L004 -> UPR-004 Introduce versioned release process and rollback-safe artifacts
5. L005 -> UPR-005 Add environment and config integrity validation at startup

### Wave B: Security Hardening

6. L006 -> UPR-010 Replace static bearer token with pluggable auth providers
7. L007 -> UPR-011 Add namespace-scoped RBAC authorization
8. L008 -> UPR-012 Add key/token rotation and revocation support
9. L009 -> UPR-013 Encrypt index and sensitive artifacts at rest
10. L010 -> UPR-014 Add TLS and reverse-proxy deployment guidance with secure defaults
11. L011 -> UPR-015 Add immutable audit log mode for security-sensitive actions
12. L012 -> UPR-016 Generate SBOM and add supply-chain scanning in CI
13. L013 -> UPR-017 Expand abuse protections (IP throttling, burst controls, anomaly hooks)
14. L014 -> UPR-018 Add sensitive-data redaction policy for logs and responses

### Wave C: Reliability, SRE, and Operations

15. L015 -> UPR-020 Add distinct readiness/liveness/startup endpoints
16. L016 -> UPR-021 Standardize structured logs with correlation IDs
17. L017 -> UPR-022 Expand metrics to SRE-grade dimensions
18. L018 -> UPR-023 Add OpenTelemetry tracing support
19. L019 -> UPR-024 Define SLOs and alerting policies
20. L020 -> UPR-025 Implement backup/restore with verified integrity
21. L021 -> UPR-026 Add disaster recovery drills and RTO/RPO targets
22. L022 -> UPR-027 Add graceful shutdown and zero-downtime deployment safeguards
23. L023 -> UPR-028 Add ingest idempotency and duplicate-job suppression
24. L024 -> UPR-029 Add distributed rate-limit backend option

### Wave D: Performance and Scale

25. L025 -> UPR-030 Build large-corpus benchmark suite and budgets
26. L026 -> UPR-031 Add index compaction and maintenance tooling
27. L027 -> UPR-032 Introduce queue-based async ingestion workers
28. L028 -> UPR-033 Add query and embedding cache layers with invalidation policy
29. L029 -> UPR-034 Add ANN/vector backend integrations for larger scale
30. L030 -> UPR-035 Optimize retrieval pipeline stage timings
31. L031 -> UPR-036 Add per-tenant resource quotas and isolation controls
32. L032 -> UPR-037 Add memory and CPU guardrails for worst-case inputs

### Wave E: Evaluation and Answer Quality

33. L033 -> UPR-040 Replace synthetic-only eval corpus with domain-diverse real corpora
34. L034 -> UPR-041 Add adversarial and no-answer evaluation set
35. L035 -> UPR-042 Add citation faithfulness and grounding score gates
36. L036 -> UPR-043 Add evaluation drift dashboard and trend reports
37. L037 -> UPR-044 Add human review workflow for gate overrides
38. L038 -> UPR-045 Add canary release evaluation against production-like traffic samples
39. L039 -> UPR-046 Add provider/model drift controls for AI-enabled modes
40. L040 -> UPR-047 Add multilingual retrieval/evaluation coverage

### Wave F: Universal Usefulness and Feature Completeness

41. L041 -> UPR-050 Add connector framework for external knowledge sources
42. L042 -> UPR-051 Add first-party enterprise connectors roadmap and stubs
43. L043 -> UPR-052 Add structured-data ingestion and schema-aware retrieval
44. L044 -> UPR-053 Expand parser coverage and resilience
45. L045 -> UPR-054 Add language- and format-aware chunking presets
46. L046 -> UPR-055 Add richer metadata extraction and policy-driven filtering
47. L047 -> UPR-056 Implement cross-index federation planner
48. L048 -> UPR-057 Add policy controls for answer style and safety mode
49. L049 -> UPR-058 Add query intent classification and rewrite pipeline
50. L050 -> UPR-059 Add retrieval explanation metadata for end-users

### Wave G: Governance, Compliance, and Risk Management

51. L051 -> UPR-070 Add data retention, deletion, and legal-hold policy controls
52. L052 -> UPR-071 Add user/tenant data export and deletion workflows
53. L053 -> UPR-072 Build compliance control mapping (SOC2/ISO-style baseline)
54. L054 -> UPR-073 Establish recurring threat modeling and security review cadence
55. L055 -> UPR-074 Add recurring penetration test and remediation workflow
56. L056 -> UPR-075 Add incident response runbooks and tabletop exercises

### Wave H: DX, API Productization, and Maintainability

57. L057 -> UPR-080 Publish OpenAPI contract and generated client SDKs
58. L058 -> UPR-081 Add explicit API and config versioning policy
59. L059 -> UPR-082 Add strict config schema docs and validation examples
60. L060 -> UPR-083 Add containerized/devcontainer reproducible dev environment
61. L061 -> UPR-084 Add chaos and fault-injection test scenarios
62. L062 -> UPR-085 Add architecture fitness functions and guardrail checks
63. L063 -> UPR-086 Add performance and cost budget gates
64. L064 -> UPR-087 Add release readiness scorecard document and checklist gate

## Milestone Checkpoints

- Checkpoint M1 after L014: Security model foundations complete.
- Checkpoint M2 after L024: Reliability and operations foundations complete.
- Checkpoint M3 after L032: Performance/scale foundations complete.
- Checkpoint M4 after L040: Evaluation hardening complete.
- Checkpoint M5 after L050: Universal usefulness feature set complete.
- Checkpoint M6 after L056: Governance/compliance hardening complete.
- Checkpoint M7 after L064: Universal production promotion readiness review.

## Promotion Readiness Rule

Do not mark universal production ready until:
- all loops L001-L064 are complete
- all checkpoints M1-M7 are explicitly signed off in docs/universal-production-progress-log.md
- release gate CI is green on main for the final hardening PR
