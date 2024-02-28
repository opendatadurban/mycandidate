"""update person relationship with political_party v5

Revision ID: d7fe46b32e71
Revises: 3d6746d4c09b
Create Date: 2024-01-31 11:00:36.093843

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd7fe46b32e71'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # op.create_table('political_party',
    # sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    # sa.Column('name', sa.String(), nullable=False),
    # sa.Column('abbreviation', sa.String(), nullable=True),
    # sa.PrimaryKeyConstraint('id')
    # )

    # op.create_table('person',
    # sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    # sa.Column('name', sa.String(), nullable=False),
    # sa.Column('surname', sa.String(), nullable=False),
    # sa.Column('gender', sa.String(), nullable=True),
    # sa.Column('race', sa.String(), nullable=True),
    # sa.Column('party_id', sa.Integer(), sa.ForeignKey('political_party.id', name='fk_person_party_id'), nullable=False),
    # sa.PrimaryKeyConstraint('id')
    # )
    
    # op.create_table('constituency',
    # sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    # sa.Column('code', sa.String(), nullable=True),
    # sa.Column('name', sa.String(), nullable=True),
    # sa.PrimaryKeyConstraint('id')
    # )

    # op.create_table('province',
    # sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    # sa.Column('code', sa.String(), nullable=False),
    # sa.Column('name', sa.String(), nullable=False),
    # sa.PrimaryKeyConstraint('id')
    # )
    
    # op.create_table('ward',
    # sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    # sa.Column('name', sa.String(), nullable=False),
    # sa.Column('code', sa.String(), nullable=False),
    # sa.Column('province_id', sa.Integer(), sa.ForeignKey('province.id', name='fk_ward_province_id'), nullable=False),
    # sa.PrimaryKeyConstraint('id')
    # )

    # op.create_table('candidates',
    # sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    # sa.Column('candidate_type', sa.String(), nullable=False),
    # sa.Column('person_id', sa.Integer(), sa.ForeignKey('person.id', name='fk_candidates_person_id'), nullable=False),
    # sa.Column('party_id', sa.Integer(), sa.ForeignKey('political_party.id', name='fk_candidates_party_id'), nullable=False),
    # sa.Column('constituency_id', sa.Integer(), sa.ForeignKey('constituency.id', name='fk_candidates_constituency_id'), nullable=True),
    # sa.Column('ward_id', sa.Integer(), sa.ForeignKey('ward.id', name='fk_candidates_ward_id'), nullable=True),
    # sa.PrimaryKeyConstraint('id')
    # )

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

