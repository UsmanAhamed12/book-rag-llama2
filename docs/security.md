# Security

## Authentication

The backend uses bearer-token/JWT authentication. Protected endpoints resolve the current user from the token and user-owned resources should always be scoped by that user ID.

## Passwords

Passwords must never be stored as plaintext. Password hashing/verification belongs in the security layer. Do not log passwords, hashes, authorization headers, or access tokens.

## Secrets

Never commit `.env` or real credentials. Generate a strong `SECRET_KEY` for each environment:

```bash
openssl rand -hex 32
```

Production secrets should be supplied by the deployment platform or a secret-management system.

## Database

Use a dedicated application database/user with the minimum privileges required. Do not expose PostgreSQL publicly unless the deployment architecture explicitly requires it and network controls are applied.

## File uploads

PDF uploads are untrusted input. Production hardening should enforce file type/content validation, maximum request/file size, safe generated storage paths, filename sanitization, per-user authorization, storage quotas, and malware/security scanning where appropriate.

## CORS and HTTPS

Development may allow local frontend origins. Production should allow only the deployed frontend origin(s). Serve the application through HTTPS and never transmit bearer tokens over plaintext public HTTP.

## RAG-specific risks

Uploaded documents can contain prompt-injection-like text. Treat retrieved document content as untrusted data, clearly separate system instructions from document text, and avoid giving document text authority to change application/security rules.

## Logging

Logs should provide operational value without exposing sensitive document content, secrets, tokens, credentials, or unnecessary personal data.

## Production checklist

Before public deployment, verify HTTPS, secret rotation, restricted CORS, database least privilege, upload limits, authentication/authorization tests, dependency scanning, rate limiting, structured monitoring, backups, error sanitization, and a defined data-retention policy.