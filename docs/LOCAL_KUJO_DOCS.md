# Local Kujo documentation dogfood

This installation serves a snapshot of the published `https://docs.kujolang.ai` site from `http://127.0.0.1:8787`, in namespace `kujo_docs`. It is a private local dogfood instance, not a public production release. AI Chat's existing local service uses it through the Documentation tool.

## What is indexed

`scripts/sync_local_kujo_docs.py` discovers pages through the public sitemap, fetches only HTTPS URLs on that origin, and extracts each page's article (or main content). It keeps code indentation, headings, warnings and absolute links, excludes navigation/scripts, and writes Markdown snapshots under ignored `data/local-kujo-docs/corpus/`. Each file starts with its public source URL. The manifest records the URL, local filename, original response hash, MIME type and fetch time. Citation line ranges describe the extracted local snapshot, not the original HTML line numbers.

This uses the live published site rather than assuming that an uncommitted local checkout matches production. Python's standard library and curl are operator tooling; the search/index/API runtime remains Kujo. Hash embeddings and local JSON storage require no embedding-provider account or paid model calls.

Code examples are retained as published. Language preferences do not translate Kujo code into Python or discard unique examples. The current site does not declare `retrieval-example` equivalence groups, so ordinary documents retain their complete example content regardless of the requested language. Annotated equivalent examples can use the existing preference selection contract later.

## Use it in AI Chat

Open the existing AI Chat instance on port 4174. The enabled **Documentation** preset exposes `documentation_query`. Ask it, for example, “Use the documentation tool to explain how to install Kujo, and cite the source.” The Code examples control is optional. Source URLs are returned beside local citation paths and ranges.

The host configuration sets `AI_CHAT_RAG_URL`, `AI_CHAT_RAG_NAMESPACE`, `AI_CHAT_RAG_SUPPORTS_PREFERENCES`, `AI_CHAT_RAG_TOKEN`, and `AI_CHAT_RAG_TIMEOUT_MS=60000`. Uncached searches measured roughly 20–45 seconds on the shared host; the default 10-second adapter timeout was too short for this corpus. The local override remains bounded and does not add retries. The token lives only in the private local `.env`; it is not included in tool arguments or model messages.

## Operate the local service

The launchd label is `com.kujo.rag.docs`, with RunAtLoad and KeepAlive enabled for the current user. Its plist is in `~/Library/LaunchAgents/`. `scripts/run_local_docs_service.py` loads the private, ignored `data/local-kujo-docs/service.json` and executes the installed Kujo runtime. This file contains the bearer token and must remain mode 0600.

The API binds to loopback only, requires bearer authentication, uses a reader role and isolates the `kujo_docs` index. Ingestion is performed locally with the CLI; the configured corpus is the only API ingest root. Existing indexes and AI Chat conversations are preserved.

Refresh on demand from the RAG repository:

```sh
python3 scripts/sync_local_kujo_docs.py
python3 scripts/run_local_docs_service.py ingest --path ./data/local-kujo-docs/corpus --recursive true
launchctl kickstart -k "gui/$(id -u)/com.kujo.rag.docs"
```

Use the refresh commands sequentially and stop if either fails. No background crawling schedule has been created. Restart after ingest so the service uses the refreshed index and clears its query cache. Snapshot refresh downloads all pages successfully before replacing the prior snapshot and only removes files owned by its previous manifest.

Logs: `data/local-kujo-docs/server.log` and `server.err.log`. The private service config identifies the index path and runtime binary. To stop the service:

```sh
launchctl bootout "gui/$(id -u)/com.kujo.rag.docs"
```

RAG's previously recorded overdue threat-model review remains a public release-readiness issue. This local setup does not change its review timestamp or claim that release gate has passed.

Verified initial snapshot: 100 published pages, 184 chunks, zero ingestion errors. Unauthenticated queries returned 401; authenticated searches returned installation/quickstart and owned-agent-project documentation with source URLs. The real AI Chat RAG adapter completed a cold query in 43.552 seconds during concurrent verification work. Extraction tests and the focused adapter tests passed.
