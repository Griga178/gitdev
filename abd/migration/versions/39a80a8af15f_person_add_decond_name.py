"""person add decond_name

Revision ID: 39a80a8af15f
Revises: 4848c8a8e828
Create Date: 2023-10-13 12:22:34.057642

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '39a80a8af15f'
down_revision: Union[str, None] = '4848c8a8e828'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('person', sa.Column('second_name', sa.Text))


def downgrade() -> None:
    op.drop_column('person', 'second_name')
