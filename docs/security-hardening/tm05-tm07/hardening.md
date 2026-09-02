# Security Hardening Review: RAG TM-05 and TM-07 residual boundaries

## Evidence Basis

This review derives from the current RAG threat-model packet, the Qdrant save
path and regression coverage, and Kujo's current filesystem APIs. I inspected
the source at RAG `77e6174` and Kujo `2a5612c`; this is a design product, not a
claim that the residual findings are closed.

## Constraints

We must preserve existing local JSON behavior, keep the common read path
bounded, avoid platform-specific security downgrades, and prevent remote vector
updates from turning a failed save or deletion into silent divergence. No
measured latency budget was supplied, so the proposals use a balanced profile
and require benchmarks before promotion from preview to stable.

## Opportunity Portfolio

| Opportunity | Evidence | Options | Recommendation | Proposal |
| --- | --- | --- | --- | --- |
| Descriptor-relative ingest reads | TM-05 path race and Kujo filesystem APIs (E-TM, E-KUJO-FS) | Existing preflight checks; capability-style no-follow read | Add the Kujo-owned capability API, then adopt it in RAG | [Filesystem containment](proposals/descriptor-relative-ingest.md) |
| Recoverable Qdrant commits | TM-07 transaction residual and destructive sync order (E-TM, E-QSRC, E-QTEST) | Keep destructive replacement; staged generation plus atomic alias | Use staged generations and an explicit recovery journal | [Qdrant commit protocol](proposals/qdrant-recoverable-commit.md) |

## Recommendation Summary

I recommend the structural option in both cases. The current guards remain
useful tactical protection, but they cannot make a check-then-open path atomic.
Likewise, fail-closed return values do not restore a Qdrant collection that was
deleted before an upsert failed. The recommended designs move each invariant to
the operation that owns the dangerous side effect while keeping compatibility
behind explicit preview configuration during rollout.

## Next Decisions

Approve the public Kujo API name and Windows implementation mechanism, and
approve Qdrant alias support plus a required vector-dimension source for empty
generations. The implementation plans define the smallest reviewable sequence.

