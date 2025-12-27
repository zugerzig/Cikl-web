"""add notes to events

Revision ID: 9a31d6aa4825
Revises: 20250919193428
Create Date: 2025-12-27 06:04:37.841964

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a31d6aa4825'
down_revision = '20250919193428'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("events", sa.Column("notes", sa.Text(), nullable=True))

def downgrade():
    op.drop_column("events", "notes")