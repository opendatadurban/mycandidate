"""Initial migration for testing database

Revision ID: 297bd2aaa486
Revises: bac331ffde5a
Create Date: 2023-11-08 11:54:27.983896

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '297bd2aaa486'
down_revision: Union[str, None] = 'bac331ffde5a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
