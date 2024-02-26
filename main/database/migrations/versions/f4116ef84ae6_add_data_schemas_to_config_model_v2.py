"""add data_schemas to Config model v2

Revision ID: f4116ef84ae6
Revises: 8659d84acd70
Create Date: 2024-02-15 15:00:56.940592

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4116ef84ae6'
down_revision: Union[str, None] = '8659d84acd70'
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
    sa.Column('partner_name', sa.String(), nullable=True),
    sa.Column('partner_website', sa.String(), nullable=True),
    sa.Column('google_analytics_key', sa.String(), nullable=True),
    sa.Column('gtag_script', sa.String(), nullable=True),
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
