"""create user table

Revision ID: 4848c8a8e828
Revises: eb127250cd34
Create Date: 2023-10-13 12:14:56.942137

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4848c8a8e828'
down_revision: Union[str, None] = 'eb127250cd34'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('user')
