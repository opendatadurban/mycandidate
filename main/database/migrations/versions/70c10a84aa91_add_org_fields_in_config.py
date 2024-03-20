"""add org fields in config

Revision ID: 70c10a84aa91
Revises: f4116ef84ae6
Create Date: 2024-03-20 09:44:44.905328

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '70c10a84aa91'
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
    sa.Column('partner_name', sa.String(), nullable=True),
    sa.Column('partner_website', sa.String(), nullable=True),
    sa.Column('google_analytics_key', sa.String(), nullable=True),
    sa.Column('gtag_script', sa.String(), nullable=True),
    sa.Column('organization_name', sa.String(), nullable=True),
    sa.Column('organization_link', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('site_settings')
