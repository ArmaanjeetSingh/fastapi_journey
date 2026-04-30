"""rename category id in expenses

Revision ID: c3d0dfd8357c
Revises: aef8cf4a14d8
Create Date: 2026-04-26 10:01:25.378191

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3d0dfd8357c'
down_revision: Union[str, Sequence[str], None] = 'aef8cf4a14d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('expenses', 'categoy_id', new_column_name='category_id')

def downgrade() -> None:
    """Downgrade schema."""
    pass
