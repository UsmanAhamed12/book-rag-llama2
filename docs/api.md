# API Guide

The backend is a FastAPI application with versioned routes under `/api/v1`.
The deployed readiness endpoint is `GET /api/v1/health/`.

## Interactive documentation

When the backend is running locally, FastAPI exposes generated OpenAPI documentation at:

```text
http://127.0.0.1:8000/docs
```

Use the generated documentation as the canonical request/response reference for the exact checked-out version.

## Route areas

| Method | Path | Authentication | Purpose |
|---|---|---|---|
| `GET` | `/` | No | Container/load-balancer liveness response |
| `GET` | `/api/v1/health/` | No | API readiness response |
| `POST` | `/api/v1/auth/register` | No | Create a user |
| `POST` | `/api/v1/auth/login` | No | Issue a bearer token |
| `POST` | `/api/v1/upload/` | Bearer token | Upload and synchronously ingest a PDF |
| `GET` | `/api/v1/documents/` | Bearer token | List the current user's documents |
| `DELETE` | `/api/v1/documents/{document_id}` | Bearer token | Delete an owned document and its vectors |
| `POST` | `/api/v1/chat/sessions/` | Bearer token | Create a chat session |
| `GET` | `/api/v1/chat/sessions/` | Bearer token | List owned chat sessions |
| `GET` | `/api/v1/chat/sessions/{session_id}` | Bearer token | Read one owned session |
| `GET` | `/api/v1/chat/sessions/{session_id}/messages` | Bearer token | List session messages |
| `PATCH` | `/api/v1/chat/sessions/{session_id}` | Bearer token | Rename a session |
| `DELETE` | `/api/v1/chat/sessions/{session_id}` | Bearer token | Delete a session |
| `POST` | `/api/v1/chat/` | Bearer token | Ask a grounded question |

### Authentication

Registration and login routes create users and issue JWT bearer tokens.

### Upload

The upload endpoint accepts a PDF, saves it, determines PDF metadata, creates the PostgreSQL document record, runs ingestion/indexing, and attempts document-profile generation.

Duplicate file hashes are rejected.

Upload and ingestion currently happen in the request lifecycle. Large PDFs can therefore take longer than ordinary API requests; clients should display an in-progress state and use an appropriate request timeout.

### Documents

Authenticated document routes provide user-scoped document listing and deletion. Document selection is also used to scope RAG retrieval.

### Chat sessions

Authenticated session routes support creating/listing sessions, retrieving a session, reading messages, renaming a session, and deleting a session.

### Chat

The chat endpoint validates the session belongs to the authenticated user and then uses either document-profile summarization or the normal RAG path. Normal responses contain an answer plus structured source references.

A source reference contains:

```json
{
  "reference": "S1",
  "file_name": "example.pdf",
  "page_number": 12,
  "chunk_number": 3,
  "score": 0.91
}
```

## Authentication header

Protected endpoints require:

```text
Authorization: Bearer <access-token>
```

The frontend stores the returned token in browser storage and sends it with protected requests. Do not log or expose bearer tokens.

## Example health check

```bash
curl http://127.0.0.1:8000/api/v1/health/
```

Expected response:

```json
{"status":"healthy","service":"book-rag-api"}
```

## Error behavior

FastAPI uses HTTP status codes and structured error details. Examples include unauthorized/expired authentication, missing resources, and duplicate PDF upload conflicts.

## API design guidance

Keep HTTP validation/serialization in route/schema layers and business logic in services/pipelines. New endpoints should use explicit Pydantic request/response models wherever practical and remain strictly typed.
