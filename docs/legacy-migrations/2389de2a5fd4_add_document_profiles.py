"""add document profiles

Revision ID: 2389de2a5fd4
Revises: 557acb9e2c28
Create Date: 2026-08-18 01:55:31.904529
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op


revision: str = "2389de2a5fd4"
down_revision: str | Sequence[str] | None = "557acb9e2c28"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add stored document profile fields."""

    op.add_column(
        "documents",
        sa.Column(
            "summary",
            sa.Text(),
            nullable=True,
        ),
    )

    op.add_column(
        "documents",
        sa.Column(
            "topics",
            sa.JSON(),
            nullable=True,
        ),
    )

    # Existing documents already exist, so add this
    # as nullable before backfilling.
    op.add_column(
        "documents",
        sa.Column(
            "summary_status",
            sa.String(length=30),
            nullable=True,
        ),
    )

    # Existing indexed documents need a valid status.
    op.execute(
        """
        UPDATE documents
        SET summary_status = 'pending'
        WHERE summary_status IS NULL
        """
    )

    # Now enforce the model constraint.
    op.alter_column(
        "documents",
        "summary_status",
        existing_type=sa.String(length=30),
        nullable=False,
    )


def downgrade() -> None:
    """Remove stored document profile fields."""

    op.drop_column(
        "documents",
        "summary_status",
    )

    op.drop_column(
        "documents",
        "topics",
    )

    op.drop_column(
        "documents",
        "summary",
    )