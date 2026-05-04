"""add phone col

Revision ID: 3ff2eac02687
Revises: 
Create Date: 2026-05-01 07:48:16.617435

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ff2eac02687'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users",sa.Column("phone",sa.Integer()))


def downgrade() -> None:
    op.drop_column("users","phone")
