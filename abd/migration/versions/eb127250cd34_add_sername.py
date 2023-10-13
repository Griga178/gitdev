"""add sername

Revision ID: eb127250cd34
Revises: 9f2abbd25b3b
Create Date: 2023-10-13 11:42:49.645103

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eb127250cd34'
down_revision: Union[str, None] = '9f2abbd25b3b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # op.create_table(
    #     'user',
    #     sa.Column('id', sa.Integer, primary_key=True),
    #     sa.Column('username', sa.String(), nullable=False),
    #     sa.Column('email', sa.String(), nullable=False)
    # )
    # op.add_column('person', sa.Column('second_name', sa.Text))

    pass
def downgrade() -> None:
    # op.drop_table('user')
    pass
