"""init

Revision ID: be1eb9cf43f2
Revises:
Create Date: 2025-02-12 22:19:06.425170

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "be1eb9cf43f2"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "role",
        sa.Column("uuid", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("uuid"),
        sa.UniqueConstraint("uuid"),
    )
    op.create_table(
        "users",
        sa.Column("uuid", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.Column("role_id", sa.Uuid(), nullable=True),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["role.uuid"],
        ),
        sa.PrimaryKeyConstraint("uuid"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("uuid"),
    )


def downgrade() -> None:
    op.drop_table("users")
    op.drop_table("role")
