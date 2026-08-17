"""add title and updated_at to chat sessions

Revision ID: f21b1bacccce
Revises: 9bf24a1ef9de
Create Date: 2026-08-17 21:12:02.758542
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op


revision: str = "f21b1bacccce"
down_revision: str | Sequence[str] | None = "9bf24a1ef9de"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add title and updated_at to chat sessions."""

    # Add nullable first because existing rows already exist.
    op.add_column(
        "chat_sessions",
        sa.Column(
            "title",
            sa.String(length=255),
            nullable=True,
        ),
    )

    op.add_column(
        "chat_sessions",
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=True,
        ),
    )

    # Backfill old sessions.
    op.execute(
        """
        UPDATE chat_sessions
        SET title = 'New Chat'
        WHERE title IS NULL
        """
    )

    op.execute(
        """
        UPDATE chat_sessions
        SET updated_at = created_at
        WHERE updated_at IS NULL
        """
    )

    # Enforce NOT NULL after backfilling.
    op.alter_column(
        "chat_sessions",
        "title",
        existing_type=sa.String(length=255),
        nullable=False,
    )

    op.alter_column(
        "chat_sessions",
        "updated_at",
        existing_type=sa.DateTime(),
        nullable=False,
    )


def downgrade() -> None:
    """Remove title and updated_at from chat sessions."""

    op.drop_column(
        "chat_sessions",
        "updated_at",
    )

    op.drop_column(
        "chat_sessions",
        "title",
    )