#!/usr/bin/env python3
"""Bounded loopback abuse/recovery exercises; never a production attestation.

Run in a disposable checkout with KUJO_BIN pointing to the pinned runtime.
Only generated test credentials and synthetic data are used.
"""
import contextlib
import json
import os
from pathlib import Path
import secrets
import signal
import socket
import subprocess
import tempfile
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
BIN = os.environ['KUJO_BIN']
RESULTS = []
ADMIN_ROUTES = [('GET', '/metrics'), ('GET', '/retention'), ('GET', '/drain'),
                ('POST', '/retention/policy'), ('POST', '/retention/purge'),
                ('POST', '/privacy/export'), ('POST', '/privacy/delete'),
                ('POST', '/drain/start'), ('POST', '/drain/stop'),
                ('POST', '/retention/legal-hold/start'),
                ('POST', '/retention/legal-hold/stop'),
                ('POST', '/ingest/jobs/worker/tick')]


def check(label, passed, **facts):
    RESULTS.append(dict(case=label, passed=bool(passed), **facts))
    if not passed:
        raise AssertionError(label)


def request(port, method, path, token=None, body=None, headers=None):
    h = {'Content-Type': 'application/json', **(headers or {})}
    if token:
        h['Authorization'] = 'Bearer ' + token
    data = json.dumps(body or {}).encode() if method == 'POST' else None
    req = urllib.request.Request('http://127.0.0.1:%d%s' % (port, path), data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


@contextlib.contextmanager
def server(settings):
    with tempfile.TemporaryDirectory(prefix='rag-live-exercise-') as d:
        with socket.socket() as s:
            s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]
        env = {k: v for k, v in os.environ.items() if not k.startswith('KUJO_RAG_')}
        cfg = dict(ENV='development', STRICT_CONFIG='false', EMBEDDING_PROVIDER='hash',
                   VECTOR_BACKEND='local_json', NAMESPACE='exercise', INDEX_PATH=d+'/index.json',
                   API_REDACTION_ENABLED='true', API_AUTH_PROVIDER='bearer', API_RBAC_ENABLED='true', API_RBAC_DEFAULT_ROLE='reader',
                   API_RATE_LIMIT_MAX_REQUESTS='500', API_RATE_LIMIT_BURST_MAX_REQUESTS='500',
                   API_STARTUP_GRACE_MS='0', API_ACCESS_LOG='false')
        cfg.update(settings)
        env.update({'KUJO_RAG_'+k: v for k, v in cfg.items()})
        with open(d+'/server.log', 'w') as log:
            proc = subprocess.Popen([BIN, 'run', 'main.kujo', '--interpreter', 'serve', '--host', '127.0.0.1', '--port', str(port)], cwd=ROOT, env=env, stdout=log, stderr=log, start_new_session=True)
            try:
                deadline = time.monotonic()+90
                while time.monotonic() < deadline:
                    if proc.poll() is not None:
                        raise RuntimeError('Exercise server exited before readiness')
                    try:
                        if request(port, 'GET', '/health')[0] == 200:
                            break
                    except (OSError, urllib.error.URLError):
                        pass
                    time.sleep(.1)
                else:
                    raise TimeoutError('Exercise listener startup')
                yield port
            finally:
                if proc.poll() is None:
                    os.killpg(proc.pid, signal.SIGTERM)
                    try: proc.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        os.killpg(proc.pid, signal.SIGKILL); proc.wait()
                (ROOT/'results'/('api_state_%d.json' % port)).unlink(missing_ok=True)


def exercise():
    old, new = secrets.token_hex(24), secrets.token_hex(24)
    # Replay the same privileged request before and after revocation/restart.
    with server({'API_BEARER_TOKEN': old}) as port:
        check('active reader can query', request(port, 'POST', '/query', old, {'query':'test','namespace':'exercise'})[0] == 200)
        for method, path in ADMIN_ROUTES:
            status, text = request(port, method, path, old, {'namespace':'exercise'}, {'X-Kujo-Role':'admin','X-Kujo-Namespace':'*'})
            check('reader cannot forge admin '+path, status == 403 and 'rbac_forbidden' in text, status=status)
        check('anonymous query denied', request(port,'POST','/query',body={'query':'test'})[0] == 401)
        status, text = request(port, 'POST', '/query', old, {'query':'test','namespace':'other'})
        check('cross namespace denied', status == 403 and 'rbac_namespace_forbidden' in text)
    for slot, settings in [('current', {'API_BEARER_TOKEN':old,'API_BEARER_TOKEN_NEXT':new}),
                           ('next', {'API_BEARER_TOKEN':new,'API_BEARER_TOKEN_NEXT':old})]:
        with server({**settings, 'API_BEARER_REVOKED_TOKENS':old}) as port:
            for method, path in ADMIN_ROUTES:
                status, text = request(port, method, path, old, {'namespace':'exercise'})
                check('revoked '+slot+' replay '+path, status == 403 and 'revoked_token' in text, status=status)
            check('replacement credential works '+slot, request(port,'POST','/query',new,{'query':'test','namespace':'exercise'})[0] == 200)
    # The startup health request consumes one of the three allowed requests.
    # Every changing namespace/header must still consume the socket peer bucket.
    with server({'API_BEARER_TOKEN':new, 'API_RATE_LIMIT_MAX_REQUESTS':'3', 'API_RATE_LIMIT_WINDOW_SEC':'3600'}) as port:
        statuses=[]
        for i in range(8):
            statuses.append(request(port,'POST','/query',new,{'query':'test','namespace':'tenant'+str(i)}, {'X-Forwarded-For':'192.0.2.'+str(i),'X-Kujo-Namespace':'tenant'+str(i)})[0])
        check('namespace and forwarded-IP hopping remains rate limited', statuses[:2] == [403]*2 and statuses[2:] == [429]*6, statuses=statuses)
    # Real readiness degradation and recovery through independent restarts.
    for forced in ('true','false'):
        with server({'API_BEARER_TOKEN':new,'API_READINESS_FORCE_UNREADY':forced}) as port:
            live=request(port,'GET','/live')[0]; ready=request(port,'GET','/ready')[0]
            check('outage readiness '+forced, live == 200 and ready == (503 if forced == 'true' else 200), live=live, ready=ready)


if __name__ == '__main__':
    completed = False
    try:
        exercise()
        completed = True
    finally:
        print(json.dumps({'scope':'local loopback; automated operator; no external infrastructure or human tabletop', 'results':RESULTS, 'ok':completed and bool(RESULTS) and all(r['passed'] for r in RESULTS)}, indent=2))
