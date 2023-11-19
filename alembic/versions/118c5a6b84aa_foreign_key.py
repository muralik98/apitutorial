"""Foreign Key 

Revision ID: 118c5a6b84aa
Revises: d7b94fc50ee5
Create Date: 2023-11-19 16:19:57.274706

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '118c5a6b84aa'
down_revision: Union[str, None] = 'd7b94fc50ee5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('orm_posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="orm_posts", referent_table="users", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="orm_posts")
    op.drop_column('orm_posts', 'owner_id')
    pass
