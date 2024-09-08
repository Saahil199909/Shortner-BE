"""creating model for short url detail

Revision ID: 376a90eb8e7c
Revises: 2b336e01c521
Create Date: 2024-08-23 21:18:18.922288

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '376a90eb8e7c'
down_revision: Union[str, None] = '2b336e01c521'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('short_link_details',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('short_key', sa.String(), nullable=False),
    sa.Column('device', sa.String(), nullable=True),
    sa.Column('client_ip', sa.String(), nullable=True),
    sa.Column('country', sa.String(), nullable=True),
    sa.Column('city', sa.String(), nullable=True),
    sa.Column('browsers', sa.String(), nullable=True),
    sa.Column('OS', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('short_link_details')
    # ### end Alembic commands ###
