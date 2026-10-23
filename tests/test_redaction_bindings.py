#!/usr/bin/env python3
"""Exercise private redaction helpers without expanding the public module API."""
import os
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[1]
checks = r'''
from src.tests_helpers import assert_true
mut cfg := {"api_redaction_enabled": true, "api_redaction_values": ["private-value"]}
mut i := 71
mut out := "caller"
mut value_keys := ["caller"]
mut payload := {"before":"safe", "nested":[{"password":"hidden", "safe":"keep"}, ["private-value", "plain"]], "after":"safe"}
mut result := redact_map(payload, cfg)
assert_true(result["before"] == "safe")
assert_true(result["after"] == "safe")
assert_true(result["nested"][0]["password"] == "[REDACTED]")
assert_true(result["nested"][0]["safe"] == "keep")
assert_true(result["nested"][1][0] == "[REDACTED]")
assert_true(result["nested"][1][1] == "plain")
assert_true(i == 71)
assert_true(out == "caller")
assert_true(value_keys[0] == "caller")
mut scalar_cfg := {"api_redaction_enabled":true, "api_redaction_keys":"password", "api_redaction_values":"private-value", "api_redaction_mask":""}
mut scalar_result := redact_map({"password":"secret", "safe":"private-value", "plain":"ok", "number":4, "flag":false}, scalar_cfg)
assert_true(scalar_result["password"] == "[REDACTED]")
assert_true(scalar_result["safe"] == "[REDACTED]")
assert_true(scalar_result["plain"] == "ok")
assert_true(scalar_result["number"] == 4)
assert_true(scalar_result["flag"] == false)
mut disabled := redact_map({"password":"unchanged"},{"api_redaction_enabled":false})
assert_true(disabled["password"] == "unchanged")
print("nested redaction and caller binding checks: ok")
'''
# Assemble from the actual implementation, not a copied helper that can drift.
with tempfile.NamedTemporaryFile(mode='w', suffix='.kujo', prefix='redaction_test_', dir=root, delete=False) as f:
    path = Path(f.name)
    f.write((root/'src/query_api.kujo').read_text()+checks)
try:
    for mode in (['--interpreter'], []):
        result = subprocess.run([os.environ['KUJO_BIN'], 'run', str(path), *mode], cwd=root, capture_output=True, text=True, timeout=20)
        if result.returncode or 'nested redaction and caller binding checks: ok' not in result.stdout:
            raise AssertionError(result.stderr or result.stdout)
        print(('interpreter' if mode else 'bridge') + ': passed')
finally:
    path.unlink()
