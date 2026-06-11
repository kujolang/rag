# Connector Framework

## Purpose

The connector framework stages external knowledge sources into a local ingestion root and then builds a searchable index using the standard RAG ingest pipeline.

## Connector Contract

Each connector entry in `config/connectors_ingest_sources.json` follows:

- `id`: stable connector identifier
- `type`: connector implementation (`git_repo`, `http_docs`, `plugin_script`)
- `enabled`: optional toggle (default `true`)

Type-specific fields:

- `git_repo`
  - `source_path` or `repo_url` (one required)
  - `branch` (used when cloning from `repo_url`)
- `http_docs`
  - `urls` (required array)
  - `headers` (optional key/value request headers)
- `plugin_script`
  - `runner_script` (required Kujo script path)
  - `payload` (optional plugin-specific settings)
  - `timeout_ms` (optional timeout override, default `180000`)

`plugin_script` connectors run with a stable runtime contract via environment variables:

- `KUJO_RAG_CONNECTOR_PLUGIN_PAYLOAD_PATH` points to the connector payload JSON.
- `KUJO_RAG_CONNECTOR_PLUGIN_OUTPUT_PATH` points to where the plugin should write its JSON result.

Plugin JSON output contract:

- `ok` (bool)
- `error` (string)
- `message` (string)
- `details` (dict)

## Lifecycle

1. Load connector config.
2. Normalize connector specs and IDs.
3. Stage each connector into `results/connector_sources/<connector_id>`.
4. Build/update `results/connector_index.json` from the staged root.
5. Emit connector ingest report `results/connector_ingest_report.json`.

## Script

Run:

```bash
kujo run scripts/run_connector_ingest.kujo --interpreter
```

## Environment Overrides

- `KUJO_RAG_CONNECTOR_CONFIG_PATH`
- `KUJO_RAG_CONNECTOR_STAGING_ROOT`
- `KUJO_RAG_CONNECTOR_INDEX_PATH`
- `KUJO_RAG_CONNECTOR_REPORT_PATH`
- `KUJO_RAG_CONNECTOR_EMBEDDING_PROVIDER`
- `KUJO_RAG_CONNECTOR_PLUGIN_KUJO_BIN`

## Failure Modes

Connector stage failures return structured connector-level errors and fail the gate:

- missing connector source (`git_repo` without `source_path`/`repo_url`)
- git clone/copy failures
- HTTP fetch failures
- empty successful connector set

## Validation

- `kujo run tests/test_connector_framework.kujo --interpreter`
- `kujo run scripts/run_connector_ingest.kujo --interpreter`
- `kujo run tests/test_connector_plugin_stub.kujo --interpreter`

## Enterprise Connector Roadmap

Roadmap and plugin onboarding assets:

- `config/enterprise_connector_roadmap.json`
- `config/connectors_enterprise_stubs.json`
- `scripts/connectors/example_enterprise_connector_stub.kujo`
- `docs/connectors-enterprise-roadmap.md`
