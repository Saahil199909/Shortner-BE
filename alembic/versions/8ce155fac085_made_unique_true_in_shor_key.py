"""made unique = true in shor key

Revision ID: 8ce155fac085
Revises: 6230936a4cc7
Create Date: 2024-08-25 14:10:23.700580

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8ce155fac085'
down_revision: Union[str, None] = '6230936a4cc7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'five_generator', ['short_key'])
    op.create_unique_constraint(None, 'six_generator', ['short_key'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'six_generator', type_='unique')
    op.drop_constraint(None, 'five_generator', type_='unique')
    # ### end Alembic commands ###
