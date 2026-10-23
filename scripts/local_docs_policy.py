"""Fail closed if the private documentation service leaves its local-only scope."""
from pathlib import Path


def validate_local_config(config, root):
    if (Path(root) / '.env').exists():
        raise ValueError('Local-only service uses service.json exclusively; remove the competing .env file')
    env = config.get('environment', {})
    required = {
        'KUJO_RAG_API_HOST': '127.0.0.1',
        'KUJO_RAG_API_ALLOW_NON_LOOPBACK': 'false',
        'KUJO_RAG_API_AUTH_PROVIDER': 'bearer',
        'KUJO_RAG_API_RBAC_ENABLED': 'true',
        'KUJO_RAG_API_RBAC_DEFAULT_ROLE': 'reader',
        'KUJO_RAG_EMBEDDING_PROVIDER': 'hash',
        'KUJO_RAG_VECTOR_BACKEND': 'local_json',
    }
    for name, value in required.items():
        if env.get(name, '').lower() != value:
            raise ValueError('Local-only service requires ' + name + '=' + value)
    if not env.get('KUJO_RAG_API_BEARER_TOKEN', '').strip():
        raise ValueError('Local-only service requires a private bearer credential')
    if env.get('KUJO_RAG_API_CORS_ENABLED', 'false').lower() != 'false':
        raise ValueError('Local-only service requires CORS disabled')
    if env.get('KUJO_RAG_API_RBAC_POLICY_JSON', '').strip():
        raise ValueError('Local-only service requires the built-in reader policy')
    if env.get('KUJO_RAG_NAMESPACE', '').strip() in ('', 'default'):
        raise ValueError('Local-only service requires an explicit namespace')
    data = (Path(root) / 'data/local-kujo-docs').resolve()
    for name in ('KUJO_RAG_INDEX_PATH', 'KUJO_RAG_API_INGEST_ALLOWED_ROOTS'):
        path = Path(env.get(name, '')).resolve()
        if not str(env.get(name, '')).strip() or data not in path.parents:
            raise ValueError('Local-only service requires a path inside its private data directory: ' + name)
    return env
