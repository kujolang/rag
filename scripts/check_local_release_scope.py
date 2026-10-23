"""Reject a release that claims broader support than the approved local scope."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
profile = json.loads((root/'config/release_scope.json').read_text())
assert profile['scope'] == 'local-only', 'Hosted releases require a separately reviewed promotion policy'
assert profile['hosted_production_supported'] is False
assert profile['network_boundary'] == 'loopback-only'
assert profile['candidate_version'] == (root/'VERSION').read_text().strip()
assert (root/profile['review_document']).is_file()
for path in ['docs/penetration-test-report.md', 'docs/incident-local-exercises-2026-10-22.md', '.github/workflows/production-readiness.yml']:
    assert (root/path).is_file(), path
print('Local-only release scope verified; no hosted production attestation claimed.')
