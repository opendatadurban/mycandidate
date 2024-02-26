"""add data_schemas to Config model

Revision ID: 8659d84acd70
Revises: d7fe46b32e71
Create Date: 2024-02-15 10:22:40.146288

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8659d84acd70'
down_revision: Union[str, None] = 'd7fe46b32e71'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('site_settings',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('title_short', sa.String(), nullable=True),
    sa.Column('navbar_logo', sa.String(), nullable=True),
    sa.Column('favicon_logo', sa.String(), nullable=True),
    sa.Column('primary_color', sa.String(), nullable=True),
    sa.Column('secondary_color', sa.String(), nullable=True),
    sa.Column('data_schemas', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    # op.drop_table('political_party')
    # op.drop_table('person')
    # op.drop_table('constituency')
    # op.drop_table('province')
    # op.drop_table('ward')
    # op.drop_table('candidates')
    op.drop_table('site_settings')
