"""add user ownership to documents

Revision ID: 9bf24a1ef9de
Revises: 27a19729aed5
Create Date: 2026-08-09 19:01:36.757564

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "9bf24a1ef9de"
down_revision: Union[str, Sequence[str], None] = "27a19729aed5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # 1. Add user_id temporarily as nullable.
    op.add_column(
        "documents",
        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    # 2. Assign existing documents to the existing user.
    op.execute(
        """
        UPDATE documents
        SET user_id = 1
        WHERE user_id IS NULL
        """
    )

    # 3. Make user_id mandatory.
    op.alter_column(
        "documents",
        "user_id",
        existing_type=sa.Integer(),
        nullable=False,
    )

    # 4. Add foreign key.
    op.create_foreign_key(
        "fk_documents_user_id_users",
        "documents",
        "users",
        ["user_id"],
        ["id"],
    )

    # 5. Add index.
    op.create_index(
        "ix_documents_user_id",
        "documents",
        ["user_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        "ix_documents_user_id",
        table_name="documents",
    )

    op.drop_constraint(
        "fk_documents_user_id_users",
        "documents",
        type_="foreignkey",
    )

    op.drop_column(
        "documents",
        "user_id",
    )