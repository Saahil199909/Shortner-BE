"""chnages nullable to False

Revision ID: 6230936a4cc7
Revises: 0a2f776eebbc
Create Date: 2024-08-25 12:47:13.497348

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6230936a4cc7'
down_revision: Union[str, None] = '0a2f776eebbc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('five_generator', 'short_key',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('six_generator', 'short_key',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('six_generator', 'short_key',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('five_generator', 'short_key',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
