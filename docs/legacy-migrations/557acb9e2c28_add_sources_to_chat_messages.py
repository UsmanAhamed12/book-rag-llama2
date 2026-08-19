"""add sources to chat messages

Revision ID: 557acb9e2c28
Revises: f21b1bacccce
Create Date: 2026-08-17 22:41:58.535618
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op


revision: str = "557acb9e2c28"
down_revision: str | Sequence[str] | None = "f21b1bacccce"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add persisted sources to chat messages."""

    op.add_column(
        "chat_messages",
        sa.Column(
            "sources",
            sa.JSON(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Remove persisted sources from chat messages."""

    op.drop_column(
        "chat_messages",
        "sources",
    )