# Encryption At Rest

## Overview

Kujo RAG supports optional encryption for persisted indexes and other
content-bearing local artifacts using OpenSSL.

When enabled, the index file is written as an encrypted envelope:

- `format`: `kujo_rag_encrypted_index_v1`
- `algorithm`: `openssl_aes_256_cbc_pbkdf2_base64_etm_hmac_sha256`
- `ciphertext`: encrypted payload
- `integrity`: key-bound encrypt-then-MAC tag checked before decryption

Without a valid key, encrypted payloads cannot be loaded.

The same key contract protects privacy exports, deletion preflight/receipt
artifacts, and content-bearing API runtime state with the
`kujo_rag_encrypted_artifact_v1` envelope. Writes are atomic and fail closed in
strict/production mode.

## Configuration

Environment variables:

- `KUJO_RAG_AT_REST_ENCRYPTION_ENABLED=true|false`
- `KUJO_RAG_AT_REST_ENCRYPTION_KEY=<passphrase>`
- `KUJO_RAG_AT_REST_ENCRYPTION_KEY_FILE=<path to file containing passphrase>`
- `KUJO_RAG_AT_REST_ENCRYPTION_OPENSSL_BIN=openssl`

Key resolution order:

1. `KUJO_RAG_AT_REST_ENCRYPTION_KEY`
2. `KUJO_RAG_AT_REST_ENCRYPTION_KEY_FILE`

## Strict Mode

When strict mode is active (`KUJO_RAG_STRICT_CONFIG=true` or `KUJO_RAG_ENV=production`):

- at-rest encryption must be enabled
- key material must be configured via key or key file
- privacy and API runtime state cannot fall back to plaintext
- plaintext payloads and unsigned encrypted payloads are rejected rather than
  silently downgrading the configured encryption contract

Legacy encrypted envelopes without an integrity tag can be read only outside
strict/production mode. Load and re-save them with encryption enabled before
enabling strict mode.

## Failure Modes

Load fallback behavior stores an error object in `index.meta.load_error` when decryption cannot proceed:

- `encrypted_index_key_missing`
- `encrypted_index_key_file_missing`
- `encrypted_index_decrypt_failed`
- `encrypted_index_required`
- `encrypted_payload_integrity_missing`
- `encrypted_index_plaintext_invalid_json`

This keeps runtime behavior deterministic while signaling recoverable operator errors.
