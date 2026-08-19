# Database and Persistence

The project separates relational application data from vector-search data.

## PostgreSQL

PostgreSQL is used for durable application metadata such as users, uploaded-document records, chat sessions, chat messages, document status/profile information, and ownership relationships.

SQLAlchemy provides ORM access and Alembic manages schema migrations.

## ChromaDB

ChromaDB stores embeddings and chunk metadata used by semantic retrieval. It is not a replacement for relational ownership/authentication data; it serves the vector-search layer.

## Ownership

Document and chat operations must remain user-scoped. A valid resource ID alone must not grant another user access to that resource.

## Chat persistence

A chat session belongs to a user. Messages belong to a session and store role, message text, optional citation/source JSON, and creation time. Session operations include creation, listing, retrieval, rename, message retrieval, and deletion.

## Document lifecycle

A typical upload moves through states similar to:

```text
upload -> metadata record -> processing -> indexed -> profile generation -> completed
```

Failures should be represented explicitly so the UI/API can distinguish completed and failed processing.

## Migrations

Apply migrations with:

```bash
uv run alembic upgrade head
```

Create a migration after an intentional model/schema change:

```bash
uv run alembic revision --autogenerate -m "describe change"
```

Always inspect generated migration code before applying it.

## Backup considerations

A production backup plan must consider both PostgreSQL and the vector index. If Chroma can be deterministically rebuilt from retained source PDFs and metadata, PostgreSQL/source-document backups may be the primary durable source of truth; otherwise back up vector storage as well.