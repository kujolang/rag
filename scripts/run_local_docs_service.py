"""Run the local docs service or ingest using its private host configuration."""
import json
import os
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]
config = json.loads((root / 'data/local-kujo-docs/service.json').read_text())
env = dict(os.environ)
env.update(config['environment'])
os.chdir(root)
args = sys.argv[1:] or ['serve', '--host', '127.0.0.1', '--port', '8787']
os.execve(config['kujo_bin'], [config['kujo_bin'], 'run', str(root / 'main.kujo'), '--interpreter', *args], env)
