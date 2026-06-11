# OpenTelemetry Tracing Support

This document describes tracing span support and OTLP configuration surface.

## Configuration

- `KUJO_RAG_OTEL_ENABLED` (default `false`)
- `KUJO_RAG_OTEL_SERVICE_NAME` (default `kujo-rag`)
- `KUJO_RAG_OTEL_OTLP_ENDPOINT` (optional endpoint metadata)
- `KUJO_RAG_OTEL_EXPORT_MODE` (`audit` or `none`, default `audit`)

## Emitted Spans

When tracing is enabled, span events are emitted as audit events of type `trace_span` for:

- `ingest.request`
- `ingest.build_index`
- `query.request`
- `query.retrieval`
- `query.stage.tokenize`
- `query.stage.embed`
- `query.stage.retrieve`
- `query.stage.rerank`
- `query.stage.synthesize`

Each span includes:

- `service_name`
- `span_name`
- `stage`
- `request_id`
- `correlation_id`
- `duration_ms`
- `attributes`
- `otlp_endpoint` (if configured)

## Notes

- Export mode `audit` emits spans via the existing audit pipeline.
- Export mode `none` disables span export while leaving tracing config present.
