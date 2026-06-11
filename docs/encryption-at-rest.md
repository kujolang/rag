# Encryption At Rest

## Overview

Kujo RAG supports optional encryption for persisted index artifacts (`index_path`) using OpenSSL.

When enabled, the index file is written as an encrypted envelope:

- `format`: `kujo_rag_encrypted_index_v1`
- `algorithm`: `openssl_aes_256_cbc_pbkdf2_base64`
- `ciphertext`: encrypted payload

Without a valid key, encrypted payloads cannot be loaded.

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

## Failure Modes

Load fallback behavior stores an error object in `index.meta.load_error` when decryption cannot proceed:

- `encrypted_index_key_missing`
- `encrypted_index_key_file_missing`
- `encrypted_index_decrypt_failed`
- `encrypted_index_plaintext_invalid_json`

This keeps runtime behavior deterministic while signaling recoverable operator errors.
