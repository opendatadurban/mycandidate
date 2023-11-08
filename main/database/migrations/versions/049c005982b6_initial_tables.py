"""initial tables

Revision ID: 049c005982b6
Revises: 
Create Date: 2023-11-08 07:43:31.412309

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '049c005982b6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('candidate',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('province', sa.String(), nullable=True),
    sa.Column('constituency', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('sex', sa.String(), nullable=True),
    sa.Column('party', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('site_settings',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('title_short', sa.String(), nullable=True),
    sa.Column('navbar_logo', sa.String(), nullable=True),
    sa.Column('favicon_logo', sa.String(), nullable=True),
    sa.Column('primary_color', sa.String(), nullable=True),
    sa.Column('secondary_color', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('site_settings')
    op.drop_table('candidate')
    # ### end Alembic commands ###
