# Enterprise Connectors Roadmap and Onboarding

## Goal

Provide a first-party roadmap for enterprise connector coverage while keeping connector additions decoupled from core retrieval/indexing logic.

## Prioritized Connector Backlog

Roadmap source of truth:

- `config/enterprise_connector_roadmap.json`

Current priority order:

1. `wiki_confluence` (wikis)
2. `ticketing_jira` (ticketing)
3. `object_storage_s3` (object storage)
4. `database_postgres` (databases)

## Stub Catalog

Starter stub definitions are provided in:

- `config/connectors_enterprise_stubs.json`

These entries are disabled by default and demonstrate the expected `plugin_script` contract shape for enterprise integrations.

## Plugin Interface (No Core Rewrite Path)

Connector type: `plugin_script`

Required config fields:

- `id`
- `type` (`plugin_script`)
- `runner_script`

Optional config fields:

- `enabled`
- `timeout_ms`
- `payload`

Runtime environment provided to plugin scripts:

- `KUJO_RAG_CONNECTOR_PLUGIN_PAYLOAD_PATH`
- `KUJO_RAG_CONNECTOR_PLUGIN_OUTPUT_PATH`

Plugin output JSON contract:

- `ok` (bool)
- `error` (string)
- `message` (string)
- `details` (dict)

## Example Plugin Stub

Example implementation:

- `scripts/connectors/example_enterprise_connector_stub.kujo`

The example accepts `payload.source_path` and stages content into the target directory prepared by the connector runtime.

## Contributor Onboarding Steps

1. Copy one entry from `config/connectors_enterprise_stubs.json` into `config/connectors_ingest_sources.json`.
2. Set `enabled=true` and point `runner_script` to your connector plugin.
3. Implement plugin-specific logic using the payload contract and emit required JSON output.
4. Validate with `kujo run scripts/run_connector_ingest.kujo --interpreter`.
5. Add or update regression coverage in `tests/test_connector_plugin_stub.kujo`.

## Validation

- `kujo run tests/test_connector_framework.kujo --interpreter`
- `kujo run tests/test_connector_plugin_stub.kujo --interpreter`
- `kujo run scripts/run_connector_ingest.kujo --interpreter`
