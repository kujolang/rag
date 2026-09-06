"""Local HTTP MIME contract verification; no external network or credentials."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import subprocess
import tempfile
import threading

ROOT = Path(__file__).resolve().parents[1]
requests = []
class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args): pass
    def do_GET(self):
        requests.append((self.path, self.headers.get('Accept')))
        if self.path == '/redirect':
            self.send_response(302); self.send_header('Location', '/markdown.html'); self.end_headers(); return
        content_type, body = {
            '/markdown.html': ('text/markdown; charset=utf-8', '# Markdown\n```python\nprint(1)\n```'),
            '/html.md': ('text/html; charset=utf-8', '<h1>HTML</h1><p>Shared warning</p>'),
            '/plain': ('text/plain', 'Plain text content'),
            '/unsupported': ('application/json', '{"unrelated":"not a document"}'),
        }[self.path]
        self.send_response(200); self.send_header('Content-Type', content_type); self.end_headers(); self.wfile.write(body.encode())

server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
try:
    with tempfile.TemporaryDirectory(prefix='rag-mime-') as tmp:
        receipts = []
        for route, extension, calls in [('/markdown.html','.md',1),('/html.md','.html',1),('/plain','.txt',1),('/redirect','.md',2),('/unsupported',None,1)]:
            stage = Path(tmp) / ('stage-' + str(len(receipts)))
            config = Path(tmp) / 'config.json'
            config.write_text(json.dumps({'connectors':[{'id':'docs','type':'http_docs','urls':[f'http://127.0.0.1:{server.server_port}{route}']}], 'staging_root':str(stage)}))
            before = len(requests)
            executed = subprocess.run([os.environ.get('KUJO_BIN','kujo'),'run','scripts/http_document_probe.kujo','--interpreter'], cwd=ROOT,
                                      env=dict(os.environ,RAG_DOCUMENT_PROBE_CONFIG=str(config)),check=True,capture_output=True,text=True,timeout=60)
            result = json.loads(executed.stdout)
            assert len(requests)-before == calls
            assert all('text/markdown' in accept for _,accept in requests[before:])
            files = list((stage/'docs').glob('*'))
            if extension is None:
                assert result['ok'] is False and result['results'][0]['error']=='http_docs_unsupported_media_type', result
                assert files == []
            else:
                assert result['ok'] is True and len(files)==1 and files[0].suffix==extension, result
                if extension=='.md': assert '```python' in files[0].read_text()
            receipts.append({'route':route,'extension':extension,'requests':calls,'passed':True})
        output=ROOT/'results/retrieval-preferences';output.mkdir(parents=True,exist_ok=True)
        (output/'http-ingestion.json').write_text(json.dumps(receipts,indent=2)+'\n')
        print(json.dumps(receipts,indent=2))
finally:
    server.shutdown();server.server_close();thread.join()
