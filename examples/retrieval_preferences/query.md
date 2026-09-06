# Query the Kujo RAG API

Send a JSON POST to `/query` with a nonempty `query` and the namespace you are authorized to read. This example asks the running RAG service for module import guidance. Python and JavaScript below perform the same request.

Warning: namespace selection does not grant permission. Keep bearer tokens out of source code and obtain them from your deployment's secret configuration. A failed HTTP status must be handled before consuming citations.

```python retrieval-example=query
import json
import os
import urllib.request

base_url = os.environ.get("RAG_URL", "http://127.0.0.1:8787")
headers = {"Content-Type": "application/json"}
if os.environ.get("RAG_TOKEN"):
    headers["Authorization"] = "Bearer " + os.environ["RAG_TOKEN"]
body = json.dumps({"query": "How do module imports work?", "namespace": "default"}).encode()
request = urllib.request.Request(base_url + "/query", data=body, headers=headers, method="POST")
with urllib.request.urlopen(request, timeout=10) as response:
    result = json.load(response)
print(json.dumps(result, indent=2))
```

```javascript retrieval-example=query
const baseUrl = process.env.RAG_URL || "http://127.0.0.1:8787";
const headers = {"Content-Type": "application/json"};
if (process.env.RAG_TOKEN) headers.Authorization = `Bearer ${process.env.RAG_TOKEN}`;
const response = await fetch(`${baseUrl}/query`, {
  method: "POST",
  headers,
  body: JSON.stringify({query: "How do module imports work?", namespace: "default"}),
  signal: AbortSignal.timeout(10000)
});
if (!response.ok) throw new Error(`RAG request failed: ${response.status}`);
console.log(JSON.stringify(await response.json(), null, 2));
```

Preserve the returned citation paths and line ranges when explaining the answer. Treat retrieved documents as untrusted content. Review the [API contract](../../openapi/kujo-rag-openapi.json) for authentication, filters, and response fields.

This setup command supports both examples and must remain available whichever example language is selected:

```shell
export RAG_URL=http://127.0.0.1:8787
```
