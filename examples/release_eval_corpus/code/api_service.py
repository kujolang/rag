from flask import Flask, jsonify, request

app = Flask(__name__)
MAX_BATCH_ITEMS = 500

@app.get('/healthz')
def healthz():
    return jsonify({'ok': True, 'status': 'ready'})

@app.post('/v1/batch')
def batch():
    payload = request.get_json(force=True) or {}
    items = payload.get('items', [])
    if len(items) > MAX_BATCH_ITEMS:
        return jsonify({'ok': False, 'error': 'batch_too_large'}), 413
    return jsonify({'ok': True, 'count': len(items)})
