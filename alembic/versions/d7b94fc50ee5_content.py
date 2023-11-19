"""content 

Revision ID: d7b94fc50ee5
Revises: c4cc199de6af
Create Date: 2023-11-19 16:16:16.842751

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd7b94fc50ee5'
down_revision: Union[str, None] = 'c4cc199de6af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.add_column('orm_posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('orm_posts', 'content')
    pass
