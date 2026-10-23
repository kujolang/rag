"""Run the local docs service or ingest using its private host configuration."""
import json
import os
from pathlib import Path
import sys

from local_docs_policy import validate_local_config


def main():
    root = Path(__file__).resolve().parents[1]
    config_path = root / 'data/local-kujo-docs/service.json'
    if config_path.stat().st_mode & 0o077:
        raise ValueError('Private service configuration must have owner-only permissions')
    config = json.loads(config_path.read_text())
    configured = validate_local_config(config, root)
    # Do not inherit undeclared RAG settings from a launching shell or launchd.
    env = {key: value for key, value in os.environ.items() if not key.startswith('KUJO_RAG_')}
    env.update(configured)
    os.chdir(root)
    args = sys.argv[1:] or ['serve', '--host', '127.0.0.1', '--port', '8787']
    os.execve(config['kujo_bin'], [config['kujo_bin'], 'run', str(root / 'main.kujo'), '--interpreter', *args], env)


if __name__ == '__main__':
    main()
