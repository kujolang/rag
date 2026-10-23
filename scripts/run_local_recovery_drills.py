#!/usr/bin/env python3
"""Execute synthetic data-corruption and quality rollback drills in a disposable checkout."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
BIN = os.environ['KUJO_BIN']
RESULTS = []


def run(script, args=(), overrides=None, expected=0):
    env = {k:v for k,v in os.environ.items() if not k.startswith('KUJO_RAG_')}
    env.update({'KUJO_RAG_EMBEDDING_PROVIDER':'hash','KUJO_RAG_VECTOR_BACKEND':'local_json'})
    env.update(overrides or {})
    p = subprocess.run([BIN,'run',script,'--interpreter',*args], cwd=ROOT, env=env, capture_output=True, text=True, timeout=180)
    if (expected is not None and p.returncode != expected) or (expected is None and p.returncode not in (0, 1)):
        raise AssertionError('%s exited %s (expected %s): %s' % (script,p.returncode,expected,p.stdout[-5000:] or p.stderr[-1000:]))
    return json.loads(p.stdout)


def check(label, passed, **facts):
    RESULTS.append(dict(case=label,passed=bool(passed),**facts))
    if not passed: raise AssertionError(label)


def exercise():
    with tempfile.TemporaryDirectory(prefix='rag-recovery-') as name:
        d=Path(name); corpus=d/'corpus';corpus.mkdir()
        (corpus/'manual.md').write_text('The recovery sentinel is a violet lighthouse. A violet lighthouse identifies the restored recovery document.\n')
        index=d/'index.json'; cfg=d/'config.json';cfg.write_text('{"release":"known-good"}')
        env={'KUJO_RAG_INDEX_PATH':str(index),'KUJO_RAG_NAMESPACE_INDEX_ISOLATION':'false','KUJO_RAG_NAMESPACE':'exercise'}
        run('main.kujo',['ingest','--path',str(corpus)],env)
        before=run('main.kujo',['query','--question','What is the recovery sentinel?'],env)
        check('baseline query retrieves synthetic document', 'violet lighthouse' in json.dumps(before).lower())
        original=index.read_bytes()
        run('scripts/backup_state.kujo',overrides={'BACKUP_SOURCE_INDEX':str(index),'BACKUP_SOURCE_CONFIG':str(cfg),'BACKUP_OUTPUT_DIR':str(d/'backup')})
        index.write_text('{"version":999,"chunks":[]}');cfg.write_text('{"release":"corrupt"}')
        start=time.monotonic()
        restored=run('scripts/restore_state.kujo',overrides={'RESTORE_BACKUP_DIR':str(d/'backup'),'RESTORE_TARGET_INDEX':str(index),'RESTORE_TARGET_CONFIG':str(cfg)})
        after=run('main.kujo',['query','--question','What is the recovery sentinel?'],env)
        check('corruption rollback restores bytes config and query', restored.get('verified') is True and index.read_bytes()==original and json.loads(cfg.read_text())['release']=='known-good' and 'violet lighthouse' in json.dumps(after).lower(), recovery_seconds=round(time.monotonic()-start,3))
        # Corrupt the backup itself: restore must reject it before touching targets.
        (d/'backup/index.backup.json').write_text('tampered')
        snapshot=index.read_bytes()
        rejected=run('scripts/restore_state.kujo',overrides={'RESTORE_BACKUP_DIR':str(d/'backup'),'RESTORE_TARGET_INDEX':str(index),'RESTORE_TARGET_CONFIG':str(cfg)},expected=1)
        check('tampered backup rejected without changing target', rejected.get('ok') is False and index.read_bytes()==snapshot)
        # A quality recovery drill records latency gates separately: this is not a release gate pass.
        qc=d/'quality-corpus';shutil.copytree(ROOT/'examples/release_eval_corpus',qc)
        qenv={'KUJO_RAG_RELEASE_EVAL_CORPUS_PATH':str(qc),'KUJO_RAG_RELEASE_EVAL_INDEX_PATH':str(d/'quality-index.json'),'KUJO_RAG_RELEASE_EVAL_OUTPUT_PATH':str(d/'quality-report.json'),'KUJO_RAG_RELEASE_EVAL_TREND_PATH':str(d/'trend.json')}
        baseline=run('scripts/run_release_evaluation.kujo',overrides=qenv,expected=None)
        check('quality baseline passes unchanged quality thresholds', all(v for k,v in baseline['gates'].items() if 'latency' not in k), release_gate_ok=baseline['ok'], gates=baseline['gates'])
        for f in qc.rglob('*'):
            if f.is_file():f.write_text('Unrelated synthetic corruption.\n')
        degraded=run('scripts/run_release_evaluation.kujo',overrides=qenv,expected=1)
        check('quality gate detects corrupted corpus', any(not v for k,v in degraded['gates'].items() if 'latency' not in k),failed_gates=[k for k,v in degraded.get('gates',{}).items() if v is False])
        shutil.rmtree(qc);shutil.copytree(ROOT/'examples/release_eval_corpus',qc)
        recovered=run('scripts/run_release_evaluation.kujo',overrides=qenv,expected=None)
        check('quality rollback restores passing corpus',all(v for k,v in recovered['gates'].items() if 'latency' not in k), release_gate_ok=recovered['ok'], gates=recovered['gates'])


if __name__=='__main__':
    completed=False
    try:
        exercise();completed=True
    finally:
        print(json.dumps({'scope':'automated local synthetic-data exercises; no human coordination or production RTO attestation','ok':completed and all(r['passed'] for r in RESULTS),'results':RESULTS},indent=2))
