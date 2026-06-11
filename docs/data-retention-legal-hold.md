# Data Retention and Legal-Hold Controls

Kujo RAG supports namespace-scoped retention policy controls with legal-hold exemptions.

## Configuration

- `KUJO_RAG_RETENTION_POLICY_ENABLED` (default: `false`)
- `KUJO_RAG_RETENTION_DEFAULT_TTL_DAYS` (default: `365`)
- `KUJO_RAG_RETENTION_LEGAL_HOLD_ENABLED` (default: `true`)

Retention policy can also be overridden per namespace via API.

## Policy Behavior

- Retention purge evaluates chunk metadata timestamps in this order:
	- `meta.ingested_at_ms`
	- `meta.timestamp_ms`
	- `meta.timestamp`
- Chunks with timestamps older than the retention cutoff (`now - ttl_days`) are purged.
- Associated vector and lexical entries for purged chunks are removed in the same operation.
- When legal hold is active for a namespace, purge returns `legal_hold_active` and does not delete data.

## API Endpoints

All retention endpoints require admin authorization (`admin` action under RBAC).

- `GET /retention`
	- Returns global retention defaults plus current namespace override and legal-hold maps.

- `POST /retention/policy`
	- Request body fields:
		- `namespace` (optional, string)
		- `enabled` (optional, boolean)
		- `ttl_days` (optional, numeric)
	- Updates namespace retention policy override.

- `POST /retention/legal-hold/start`
	- Request body fields:
		- `namespace` (optional, string)
		- `reason` (optional, string)
	- Activates legal hold for namespace.

- `POST /retention/legal-hold/stop`
	- Request body fields:
		- `namespace` (optional, string)
		- `reason` (optional, string)
	- Releases legal hold for namespace.

- `POST /retention/purge`
	- Request body fields:
		- `namespace` (optional, string)
	- Applies retention policy for namespace unless legal hold is active.
	- Returns purge summary: cutoff timestamp and purged/retained counts.

## Operational Guidance

- Use legal hold before incident or litigation workflows that require data preservation.
- Run retention purge on a scheduled cadence aligned to compliance requirements.
- Track purge outputs and legal-hold transitions in audit/reporting systems.
