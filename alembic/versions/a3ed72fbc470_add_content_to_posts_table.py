"""add content to posts table

Revision ID: a3ed72fbc470
Revises: f087544f1662
Create Date: 2023-07-29 23:21:48.630000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3ed72fbc470'
down_revision = 'f087544f1662'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
