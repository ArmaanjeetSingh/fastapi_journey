"""phone col unique

Revision ID: 44b9dee925c5
Revises: 3ff2eac02687
Create Date: 2026-05-01 08:04:53.783127

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '44b9dee925c5'
down_revision: Union[str, Sequence[str], None] = '3ff2eac02687'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.create_unique_constraint("uq_users_phone",["phone"])

def downgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_constraint("uq_users_phone",type_="phone")
