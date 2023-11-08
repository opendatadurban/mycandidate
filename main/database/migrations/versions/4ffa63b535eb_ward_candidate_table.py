"""ward candidate table

Revision ID: 4ffa63b535eb
Revises: d1804082eaaa
Create Date: 2023-11-08 11:04:19.079151

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ffa63b535eb'
down_revision: Union[str, None] = 'd1804082eaaa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ward_candidate',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('province', sa.String(), nullable=True),
    sa.Column('local_authority', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('sex', sa.String(), nullable=True),
    sa.Column('party', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('ward_no', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ward_candidate')
    # ### end Alembic commands ###
