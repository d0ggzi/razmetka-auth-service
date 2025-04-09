"""roles data migration

Revision ID: e597ad0fd861
Revises: 1df206bcdd91
Create Date: 2025-02-12 23:47:53.848193

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm, or_

from src.domain import models

# revision identifiers, used by Alembic.
revision: str = "e597ad0fd861"
down_revision: Union[str, None] = "1df206bcdd91"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    session = orm.Session(bind=bind)
    session.execute(
        models.Role.__table__.insert().values(
            [
                {"name": "assessor"},
                {"name": "expert"},
                {"name": "customer"},
                {"name": "admin"},
            ]
        )
    )


def downgrade() -> None:
    bind = op.get_bind()
    session = orm.Session(bind=bind)
    session.delete(
        sa.delete(models.Role).where(
            or_(
                models.Role.name == "assessor",
                models.Role.name == "expert",
                models.Role.name == "customer",
                models.Role.name == "admin",
            )
        )
    )
