"""add file hash to documents

Revision ID: 27a19729aed5
Revises:
Create Date: 2026-08-09 14:16:14.941726

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "27a19729aed5"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""

    # Add the column as nullable first because existing
    # documents already exist in the database.
    op.add_column(
        "documents",
        sa.Column(
            "file_hash",
            sa.String(length=64),
            nullable=True,
        ),
    )

    # Create the unique index after the column exists.
    op.create_index(
        "ix_documents_file_hash",
        "documents",
        ["file_hash"],
        unique=True,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        "ix_documents_file_hash",
        table_name="documents",
    )

    op.drop_column(
        "documents",
        "file_hash",
    )