# Correctness Alert Runbook

1. Re-run evaluation set against current index/model snapshot.
2. Compare recent retrieval confidence/citation patterns for drift.
3. Check ingestion freshness and namespace data integrity.
4. Roll back recent corpus/model/config changes if regression is confirmed.
5. Document corrective actions and update evaluation baselines.
