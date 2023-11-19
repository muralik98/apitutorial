"""Create posts table

Revision ID: 8630961ae76a
Revises: 8b253b1e9672
Create Date: 2023-11-19 16:08:40.744329

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8630961ae76a'
down_revision: Union[str, None] = '8b253b1e9672'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('orm_posts', sa.Column('id', sa.Integer(), nullable=False,
                    primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('orm_posts')
    pass

