"""Initial migration

Revision ID: 9254f99f421d
Revises: 
Create Date: 2025-08-28 12:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, using by Alembic.
revision = '9254f99f421d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade schema - create tables if not exist."""
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(50), nullable=False, unique=True),
        sa.Column('password', sa.String(255), nullable=False)
    )

    op.create_table(
        'categories',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False, unique=True)
    )

    op.create_table(
        'expenses',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('amount', sa.Float, nullable=False),
        sa.Column('transaction_type', sa.String(10), nullable=False),
        sa.Column('category_id', sa.Integer, sa.ForeignKey('categories.id')),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('date', sa.DateTime)
    )


def downgrade() -> None:
    """Downgrade schema - drop tables."""
    op.drop_table('expenses')
    op.drop_table('categories')
    op.drop_table('users')
