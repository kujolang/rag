# Parser Coverage and Resilience

## Added Format Coverage

Parser registry now supports these extensions:

- Markdown/text: `md`, `mdx`, `markdown`, `txt`, `kujo`
- Structured: `json`, `csv`
- Markup/config/log: `html`, `htm`, `xml`, `yaml`, `yml`, `log`
- PDF: `pdf`

## Resilience and Fallback Behavior

Malformed structured files fail safely with deterministic metadata:

- malformed JSON -> `meta.parser=structured_json`, `meta.fallback=true`, `meta.error_code=malformed_json`
- malformed CSV -> `meta.parser=structured_csv`, `meta.fallback=true`, `meta.error_code=malformed_csv`

Parser sandbox guardrail:

- `KUJO_RAG_PARSER_SANDBOX_MAX_BYTES` caps parser input size.
- oversized files return deterministic fallback docs with `meta.parser=sandbox_fallback` and `meta.error_code=parser_input_too_large`.

Parser timeout guardrail:

- `KUJO_RAG_PARSER_TIMEOUT_MS` controls parser timeout budget (notably PDF shell extraction).

## Validation Corpus

- parser matrix corpus: `examples/parser_matrix_corpus`
- malformed parser corpus: `examples/malformed_parser_corpus`

## Validation

- `kujo run tests/test_parser_matrix_resilience.kujo --interpreter`
