# Config Schema Reference

This reference documents every runtime configuration key exposed by `src/config.kujo`.

Generated and validated by `scripts/run_config_schema_review.kujo`.

## Key Reference

| Key | Type | Default | Production Recommendation |
|---|---|---|---|
| api_abuse_blocklist_ips | array | [] | Use explicit allowlists tailored to tenant and environment boundaries. |
| api_access_log | bool | true | Use default unless workload or compliance requirements justify override. |
| api_anomaly_auto_block_enabled | bool | false | Keep disabled until explicitly required, then enable with controls documented. |
| api_anomaly_block_ttl_sec | int | 900 | Start with default and tune from observed latency/error-budget telemetry. |
| api_anomaly_hook_enabled | bool | false | Keep disabled until explicitly required, then enable with controls documented. |
| api_anomaly_violation_threshold | int | 3 | Use default unless workload or compliance requirements justify override. |
| api_audit_enabled | bool | false | Keep disabled until explicitly required, then enable with controls documented. |
| api_audit_external_sink_mode | string | append_file | Use default unless workload or compliance requirements justify override. |
| api_audit_path | string | ./results/security_audit.log | Use deployment-stable paths with least-privilege file permissions. |
| api_auth_provider | string | bearer | Use default unless workload or compliance requirements justify override. |
| api_bearer_revoked_tokens | array | [] | Inject via secret management; do not commit plaintext values. |
| api_bearer_token | string |  | Inject via secret management; do not commit plaintext values. |
| api_bearer_token_next | string |  | Inject via secret management; do not commit plaintext values. |
| api_cors_allowed_origins | array | [] | Use explicit allowlists tailored to tenant and environment boundaries. |
| api_cors_enabled | bool | false | Keep disabled until explicitly required, then enable with controls documented. |
| api_drain_pre_stop_ms | int | 5000 | Use default unless workload or compliance requirements justify override. |
| api_drain_reject_mutations | bool | true | Use default unless workload or compliance requirements justify override. |
| api_guardrail_ingest_max_files | int | 5000 | Use deployment-stable paths with least-privilege file permissions. |
| api_guardrail_ingest_max_total_bytes | int | 50000000 | Start with default and tune from observed latency/error-budget telemetry. |
| api_guardrail_query_max_complexity | int | 18000 | Start with default and tune from observed latency/error-budget telemetry. |
| api_guardrail_query_max_filter_keys | int | 32 | Start with default and tune from observed latency/error-budget telemetry. |
| api_guardrail_query_max_session_chars | int | 12000 | Start with default and tune from observed latency/error-budget telemetry. |
| api_host | string | 127.0.0.1 | Use default unless workload or compliance requirements justify override. |
| api_ingest_allowed_roots | array | ["."] | Use deployment-stable paths with least-privilege file permissions. |
| api_ingest_idempotency_enabled | bool | true | Keep enabled only with monitoring and rollback readiness in place. |
| api_ingest_idempotency_header | string | x-idempotency-key | Use default unless workload or compliance requirements justify override. |
| api_ingest_idempotency_window_sec | int | 900 | Start with default and tune from observed latency/error-budget telemetry. |
| api_ingest_jobs_mode | string | inline | Use default unless workload or compliance requirements justify override. |
| api_ingest_worker_batch_size | int | 1 | Use default unless workload or compliance requirements justify override. |
| api_ingest_worker_max_running | int | 1 | Start with default and tune from observed latency/error-budget telemetry. |
| api_jwt_audience | string |  | Use default unless workload or compliance requirements justify override. |
| api_jwt_clock_skew_sec | int | 60 | Use default unless workload or compliance requirements justify override. |
| api_jwt_issuer | string |  | Use default unless workload or compliance requirements justify override. |
| api_max_body_bytes | int | 1048576 | Start with default and tune from observed latency/error-budget telemetry. |
| api_max_query_chars | int | 4000 | Start with default and tune from observed latency/error-budget telemetry. |
| api_port | int | 8787 | Use default unless workload or compliance requirements justify override. |
| api_query_cache_enabled | bool | true | Keep enabled only with monitoring and rollback readiness in place. |
| api_query_cache_max_entries | int | 1000 | Start with default and tune from observed latency/error-budget telemetry. |
| api_query_cache_ttl_sec | int | 300 | Start with default and tune from observed latency/error-budget telemetry. |
| api_rate_limit_backend | string | memory | Start with default and tune from observed latency/error-budget telemetry. |
| api_rate_limit_backend_file | string | ./results/rate_limit_state.json | Use deployment-stable paths with least-privilege file permissions. |
| api_rate_limit_bucket_ttl_sec | int | 300 | Start with default and tune from observed latency/error-budget telemetry. |
| api_rate_limit_burst_max_requests | int | 30 | Start with default and tune from observed latency/error-budget telemetry. |
| api_rate_limit_burst_window_sec | int | 5 | Start with default and tune from observed latency/error-budget telemetry. |
| api_rate_limit_max_keys | int | 5000 | Start with default and tune from observed latency/error-budget telemetry. |
| api_rate_limit_max_requests | int | 120 | Start with default and tune from observed latency/error-budget telemetry. |
| api_rate_limit_window_sec | int | 60 | Start with default and tune from observed latency/error-budget telemetry. |
| api_rbac_default_role | string | admin | Use default unless workload or compliance requirements justify override. |
| api_rbac_enabled | bool | false | Keep disabled until explicitly required, then enable with controls documented. |
| api_rbac_namespace_header | string | x-kujo-namespace | Use default unless workload or compliance requirements justify override. |
| api_rbac_policy | dict | {"admin":["ingest","query","admin","export"],"reader":["query"],"writer":["ingest","query"]} | Keep schema-compatible structure; modify only through reviewed change control. |
| api_rbac_role_header | string | x-kujo-role | Use default unless workload or compliance requirements justify override. |
| api_readiness_force_unready | bool | false | Use default unless workload or compliance requirements justify override. |
| api_redaction_enabled | bool | true | Keep enabled only with monitoring and rollback readiness in place. |
| api_redaction_keys | array | ["authorization","token","api_key","apikey","secret","password","passphrase","x-api-key","set-cookie","cookie","bearer","openai_api_key"] | Use explicit allowlists tailored to tenant and environment boundaries. |
| api_redaction_mask | string | [REDACTED] | Use default unless workload or compliance requirements justify override. |
| api_redaction_values | array | [] | Use explicit allowlists tailored to tenant and environment boundaries. |
| api_startup_grace_ms | int | 1000 | Use default unless workload or compliance requirements justify override. |
| api_tenant_ingest_max_chunks_per_request | int | 50000 | Start with default and tune from observed latency/error-budget telemetry. |
| api_tenant_query_rate_max_requests | int | 120 | Start with default and tune from observed latency/error-budget telemetry. |
| api_tenant_query_rate_window_sec | int | 60 | Start with default and tune from observed latency/error-budget telemetry. |
| api_tenant_quota_enabled | bool | false | Keep disabled until explicitly required, then enable with controls documented. |
| api_tenant_storage_max_chunks | int | 200000 | Start with default and tune from observed latency/error-budget telemetry. |
| at_rest_encryption_enabled | bool | false | Keep disabled until explicitly required, then enable with controls documented. |
| at_rest_encryption_key | string |  | Use default unless workload or compliance requirements justify override. |
| at_rest_encryption_key_file | string |  | Inject via secret management; do not commit plaintext values. |
| at_rest_encryption_openssl_bin | string | openssl | Use default unless workload or compliance requirements justify override. |
| chunk_overlap | int | 150 | Use default unless workload or compliance requirements justify override. |
| chunk_presets | dict | {} | Keep schema-compatible structure; modify only through reviewed change control. |
| chunk_presets_enabled | bool | false | Keep disabled until explicitly required, then enable with controls documented. |
| chunk_size | int | 900 | Use default unless workload or compliance requirements justify override. |
| chunk_strategy | string | line | Use default unless workload or compliance requirements justify override. |
| embedding_cache_enabled | bool | true | Keep enabled only with monitoring and rollback readiness in place. |
| embedding_cache_max_entries | int | 10000 | Start with default and tune from observed latency/error-budget telemetry. |
| embedding_dims | int | 256 | Use default unless workload or compliance requirements justify override. |
| embedding_provider | string | hash | Use default unless workload or compliance requirements justify override. |
| hybrid_alpha | float | 0.65 | Use default unless workload or compliance requirements justify override. |
| hybrid_beta | float | 0.35 | Use default unless workload or compliance requirements justify override. |
| index_path | string | ./data/rag_index.json | Use deployment-stable paths with least-privilege file permissions. |
| ingest_extensions | array | ["md","mdx","markdown","txt","pdf","kujo","py","json","csv","html","htm","xml","yaml","yml","log"] | Use explicit allowlists tailored to tenant and environment boundaries. |
| max_file_bytes | int | 5000000 | Use deployment-stable paths with least-privilege file permissions. |
| namespace | string | default | Use default unless workload or compliance requirements justify override. |
| namespace_index_isolation | bool | true | Use default unless workload or compliance requirements justify override. |
| otel_enabled | bool | false | Keep disabled until explicitly required, then enable with controls documented. |
| otel_export_mode | string | audit | Use default unless workload or compliance requirements justify override. |
| otel_otlp_endpoint | string |  | Use default unless workload or compliance requirements justify override. |
| otel_service_name | string | kujo-rag | Use default unless workload or compliance requirements justify override. |
| parser_sandbox_max_bytes | int | 5000000 | Start with default and tune from observed latency/error-budget telemetry. |
| parser_timeout_ms | int | 30000 | Start with default and tune from observed latency/error-budget telemetry. |
| pdf_extractor_command | string | pdftotext | Use default unless workload or compliance requirements justify override. |
| project_root | string | . | Use deployment-stable paths with least-privilege file permissions. |
| query_expansion | bool | true | Use default unless workload or compliance requirements justify override. |
| query_intent_rewrite_enabled | bool | true | Keep enabled only with monitoring and rollback readiness in place. |
| query_retrieval_explanation_enabled | bool | false | Keep disabled until explicitly required, then enable with controls documented. |
| query_safe_response_enabled | bool | true | Keep enabled only with monitoring and rollback readiness in place. |
| query_safe_response_message | string | I cannot answer safely from the available local context. | Use default unless workload or compliance requirements justify override. |
| query_safe_response_min_overlap_ratio | float | 0.15 | Use default unless workload or compliance requirements justify override. |
| rerank_mmr_lambda | float | 0.7 | Use default unless workload or compliance requirements justify override. |
| rerank_strategy | string | none | Use default unless workload or compliance requirements justify override. |
| retention_default_ttl_days | int | 365 | Start with default and tune from observed latency/error-budget telemetry. |
| retention_legal_hold_enabled | bool | true | Keep enabled only with monitoring and rollback readiness in place. |
| retention_policy_enabled | bool | false | Keep disabled until explicitly required, then enable with controls documented. |
| runtime_environment | string | development | Set to production in production environments. |
| session_history_max_turns | int | 4 | Start with default and tune from observed latency/error-budget telemetry. |
| strict_config | bool | false | Set true for production deployments. |
| top_k | int | 6 | Use default unless workload or compliance requirements justify override. |
| vector_backend | string | local_json | Use default unless workload or compliance requirements justify override. |
| vector_backend_memory_key | string |  | Use default unless workload or compliance requirements justify override. |
| vector_backend_qdrant_api_key | string |  | Inject via secret management; do not commit plaintext values. |
| vector_backend_qdrant_collection | string | kujo_rag | Use default unless workload or compliance requirements justify override. |
| vector_backend_qdrant_fail_open | bool | true | Use default unless workload or compliance requirements justify override. |
| vector_backend_qdrant_mirror_path | string |  | Use deployment-stable paths with least-privilege file permissions. |
| vector_backend_qdrant_sync_enabled | bool | false | Keep disabled until explicitly required, then enable with controls documented. |
| vector_backend_qdrant_timeout_ms | int | 8000 | Start with default and tune from observed latency/error-budget telemetry. |
| vector_backend_qdrant_url | string |  | Use default unless workload or compliance requirements justify override. |

## Invalid Configuration Examples

Invalid config cases and expected validation errors are defined in `./config/config_validation_examples.json`.

Validate examples with:

- `kujo run scripts/run_config_schema_review.kujo --interpreter`
