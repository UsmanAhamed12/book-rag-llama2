# Docker

Docker provides a reproducible build boundary for the application and is validated by CI.

## Why Docker is used

- consistent runtime dependencies;
- reproducible builds across developer/CI/deployment environments;
- easier deployment packaging;
- isolation from host Python configuration.

## Build

Use the Docker configuration under the repository's `docker/` directory and the project CI workflow as the source of truth for the currently supported build command.

Before changing Docker configuration, ensure local backend quality checks pass so container failures are not hiding ordinary application failures.

## Runtime dependencies

The complete application also depends on services/data outside the Python process, notably PostgreSQL, Ollama, persistent Chroma storage, uploaded PDF storage, and the frontend. A production deployment must define how these components communicate and persist data.

## Environment variables

Do not bake secrets into images. Pass environment configuration at runtime using the deployment platform's environment/secret mechanism.

## Persistence

Ephemeral containers must not be the only location for durable PostgreSQL data, required uploads, or vector data. Use managed databases and/or persistent volumes according to the deployment architecture.

## Ollama note

Local development can run Ollama directly on the host. Containerized or cloud deployment needs an explicit LLM-serving architecture and sufficient compute resources rather than assuming the host-local Ollama URL will automatically be available inside a container.

## CI

A successful Docker build is one part of the repository quality gate alongside backend and frontend checks.