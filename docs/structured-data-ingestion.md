# Structured Data Ingestion and Schema-Aware Retrieval

## Purpose

Enable production ingestion of JSON and CSV data with schema metadata so retrieval can filter and rank results by schema and field context.

## Supported Structured Formats

- `json`
- `csv`

Structured files are parsed into normalized row-oriented text blocks with metadata:

- `structured` (bool)
- `structured_format` (`json` or `csv`)
- `structured_schema` (derived from filename)
- `structured_fields` (normalized field names)
- `record_count`

## Retrieval Filter Contract

`POST /query` `filters` now supports schema-aware keys:

- `structured_schema` (string or array)
- `structured_fields` (string or array)

Compatibility aliases are also accepted:

- `schema` -> `structured_schema`
- `field` -> `structured_fields`

These keys can be combined with existing filters (`path`, `extension`, `tags`).

## Field-Level Context

Citations now include structured metadata:

- `structured_schema`
- `structured_fields`

Structured snippets are row-shaped (`field: value`) so answers remain grounded to explicit field-level evidence.

## Validation

- `kujo run tests/test_structured_ingestion_retrieval.kujo --interpreter`
- `kujo run tests/test_unit.kujo --interpreter`
