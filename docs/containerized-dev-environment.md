# Containerized and Devcontainer Development Environment

This document defines the reproducible environment baseline for Kujo RAG development.

## Goals

- one-command containerized startup for clean-room onboarding
- reproducible VS Code devcontainer setup
- native/local workflow support remains available

## One-Command Container Quick Start

From repository root:

```bash
docker compose up --build
```

This starts the API server with:

- command: `kujo run main.kujo --interpreter serve`
- host binding: `0.0.0.0:8787`
- source mounted at `/workspace`

## VS Code Devcontainer

Use the provided devcontainer configuration:

- `.devcontainer/devcontainer.json`
- base image build path: `../Dockerfile`

After opening in container, `postCreateCommand` verifies runtime readiness and schema gate health.

## Native Workflow Compatibility

Local native workflow remains fully supported:

```bash
KUJO_BIN=/path/to/kujo/target/debug/kujo \
/path/to/kujo/target/debug/kujo run main.kujo --interpreter query --question "What is Kujo optimized for?"
```

No container requirement is imposed for contributors who prefer native Kujo runtime execution.

## Validation Gate

Run deterministic environment checks:

```bash
kujo run scripts/run_containerized_dev_environment_review.kujo --interpreter
```

CI workflow:

- `.github/workflows/containerized-dev-environment-review.yml`
