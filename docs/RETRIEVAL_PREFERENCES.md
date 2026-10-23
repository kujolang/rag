# Documentation example preferences

RAG can select equivalent code examples before serializing the response or constructing answer context. This is an optional Kujo request field, not an HTTP or MCP standard. It does not use `Accept-Language`, infer a task language from a file extension, or change authorization.

## Start the documentation pilot

```sh
export KUJO_RAG_MARKDOWN_EXAMPLES_ENABLED=true
export KUJO_RAG_CHUNK_SIZE=4000
export KUJO_RAG_INDEX_PATH=./data/documentation-pilot.json
kujo run main.kujo -- ingest --path ./examples/retrieval_preferences --recursive true
kujo run main.kujo -- serve --host 127.0.0.1 --port 8787
```

In another terminal:

```sh
curl -s http://127.0.0.1:8787/query -H 'Content-Type: application/json' \
  -d '{"query":"How do I query the RAG API?","retrieval_preferences":{"programming_language":"python"}}'
```

The CLI accepts `query --question "..." --programming-language python` with the same index configuration. The equivalent Python and JavaScript examples in `examples/retrieval_preferences/query.md` exercise the real RAG query API.

## Annotate alternatives deliberately

Enabling `KUJO_RAG_MARKDOWN_EXAMPLES_ENABLED` preserves original Markdown and source line numbers. Reingest after changing this setting; the parser contract participates in incremental document identity.

Use a named group for equivalent examples:

````markdown
Shared guidance and warnings.

```python retrieval-example=query
# Python implementation of the query operation
```

```javascript retrieval-example=query
// JavaScript implementation of the same operation
```
````

Selection removes a different language's block only when the same group contains the requested language. General prose, links, warnings, ungrouped setup/configuration blocks, malformed/unclosed fences, and groups without a match remain available. A language label alone does not claim that two examples are interchangeable. This avoids deleting a unique example needed to understand an operation.

The opt-in chunk profile preserves complete tagged fences and original line positions without overlap duplication. Chunk size is a target; a single complete example can exceed it, bounded by the parser document byte limit. Citation ranges refer to the original source and may include alternatives omitted from the selected excerpt. Stored vectors and ranking retain the original document evidence; selection occurs before the final ranking candidate is serialized or passed to synthesis. Existing corpus filters and namespace checks still apply.

With the setting disabled, legacy Markdown parsing remains unchanged. Previously indexed unannotated corpora remain usable and produce their ordinary results.

## Request and cache contract

`retrieval_preferences.programming_language` is trimmed and lowercased, accepts extensible `[a-z][a-z0-9_-]*` identifiers up to 64 characters, and maps `c++`/`c#` to `cpp`/`csharp`. Unknown fields and invalid values are ignored. There is no language detection, network capability probe, or retry to discover support.

The API cache includes the normalized preference alongside the existing namespace, index generation, query, filters, and session history. Equivalent casing shares a variant; different languages cannot reuse each other's selected content. Unsupported languages fall back to the original content. Empty matches remain empty. Federation applies the same preference independently within each authorized target index.

## HTTP documentation ingestion

The `http_docs` connector requests Markdown with HTML/plain-text fallbacks. For HTTP(S), the final response Content-Type determines whether the staged file is `.md`, `.html`, or `.txt`, regardless of URL suffix. Missing Content-Type uses plain text; other media types fail explicitly. Complete bodies are bounded to 5,000,000 bytes and requests to 30 seconds. Native transport preserves redirect handling and pins DNS under the runtime network policy. No programming-language header is sent to arbitrary documentation sites.

Configured local `file://` fixtures remain supported. HTTP staging names use a URL digest so different URLs with the same basename do not overwrite each other.

## Verification and measurement

Core runtime and ordinary tests require only Kujo. Optional developer HTTP measurements use Python and `tiktoken`:

```sh
python3 -m venv /tmp/rag-measurement
/tmp/rag-measurement/bin/pip install tiktoken==0.14.0
KUJO_BIN=kujo /tmp/rag-measurement/bin/python scripts/verify_retrieval_preferences.py
KUJO_BIN=kujo python3 scripts/verify_http_document_ingestion.py
```

When sibling rollout checkouts are present, the pilot also exercises Agents SDK, AI Chat, and Dispatch. Set `AGENTS_SDK_PATH`, `AI_CHAT_PATH`, `DISPATCH_PATH`, and `NODE_BIN` to explicit paths when needed. AI Chat needs its installed dependencies and patched Node 22.23.4.

Receipts in `results/retrieval-preferences/` record response bytes, exact named-tokenizer counts, latency, request counts, cache behavior, retained guidance, and original citation ranges. Captured agent/AI Chat messages measure actual model-input content, excluding provider-specific message framing. The model callbacks are local fixtures, so this measures context reduction rather than paid model quality or inference latency. Do not claim latency or quality improvements beyond these checks.

Framework/library-version selection and third-party adapters remain deferred: this corpus demonstrates language-equivalent examples, not version-equivalent semantics or external support for further request dimensions.
