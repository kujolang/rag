# Backup and Restore Integrity

This document describes backup and restore workflows with checksum verification.

## Backup

Use `scripts/backup_state.kujo` with optional environment overrides:

- `BACKUP_SOURCE_INDEX` (default `data/rag_index.json`)
- `BACKUP_SOURCE_CONFIG` (default `config/release_eval_thresholds.json`)
- `BACKUP_OUTPUT_DIR` (default `results/backups/backup-<timestamp>`)

Artifacts written:

- `index.backup.json`
- `config.backup.json`
- `manifest.json` (includes `sha256` integrity metadata)

## Restore

Use `scripts/restore_state.kujo` with:

- `RESTORE_BACKUP_DIR` (required)
- `RESTORE_TARGET_INDEX` (optional)
- `RESTORE_TARGET_CONFIG` (optional)

Restore behavior:

1. Read `manifest.json`.
2. Verify backup checksums before writing targets.
3. Restore target files only if checksum verification passes.

## Verification

- Check restore output for `verified: true`.
- Recompute file hashes and compare with manifest when auditing manually.
