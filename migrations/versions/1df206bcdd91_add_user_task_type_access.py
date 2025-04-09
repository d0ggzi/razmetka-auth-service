"""add user task-type access

Revision ID: 1df206bcdd91
Revises: be1eb9cf43f2
Create Date: 2025-02-12 23:47:05.904163

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "1df206bcdd91"
down_revision: Union[str, None] = "be1eb9cf43f2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_task_type_access",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("task_type_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.uuid"],
        ),
        sa.PrimaryKeyConstraint("user_id", "task_type_id"),
    )
    op.create_unique_constraint(None, "role", ["uuid"])
    op.alter_column("users", "role_id", existing_type=sa.UUID(), nullable=False)
    op.create_unique_constraint(None, "users", ["uuid"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
    op.alter_column("users", "role_id", existing_type=sa.UUID(), nullable=True)
    op.drop_constraint(None, "role", type_="unique")
    op.drop_table("user_task_type_access")
