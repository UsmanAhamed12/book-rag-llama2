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

### Authentication

Registration and login routes create users and issue JWT bearer tokens.

### Upload

The upload endpoint accepts a PDF, saves it, determines PDF metadata, creates the PostgreSQL document record, runs ingestion/indexing, and attempts document-profile generation.

Duplicate file hashes are rejected.

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

## Error behavior

FastAPI uses HTTP status codes and structured error details. Examples include unauthorized/expired authentication, missing resources, and duplicate PDF upload conflicts.

## API design guidance

Keep HTTP validation/serialization in route/schema layers and business logic in services/pipelines. New endpoints should use explicit Pydantic request/response models wherever practical and remain strictly typed.
