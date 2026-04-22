"""create phone_number for users column

Revision ID: d79247a963ea
Revises: 77e5b63ba6b1
Create Date: 2026-04-21 14:46:54.150899

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd79247a963ea'
down_revision: Union[str, Sequence[str], None] = '77e5b63ba6b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users',sa.Column('phone_number',sa.String(),nullable = True))


def downgrade() -> None:
    """Downgrade schema."""
    pass
