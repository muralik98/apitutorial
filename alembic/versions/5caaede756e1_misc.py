""" misc

Revision ID: 5caaede756e1
Revises: c04f2197245e
Create Date: 2023-11-19 16:35:02.963334

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5caaede756e1'
down_revision: Union[str, None] = 'c04f2197245e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('orm_posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('orm_posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('orm_posts', 'published')
    op.drop_column('orm_posts', 'created_at')
    pass
