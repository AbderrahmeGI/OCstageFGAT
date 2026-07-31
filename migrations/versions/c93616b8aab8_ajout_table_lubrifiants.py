"""Ajout table lubrifiants

Revision ID: c93616b8aab8
Revises: 56aea08c7d66
Create Date: 2026-07-17 18:14:21.275960
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c93616b8aab8'
down_revision = '56aea08c7d66'
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        'lubrifiants',

        sa.Column('id', sa.Integer(), primary_key=True),

        sa.Column('nom', sa.String(100), nullable=False, unique=True),

        sa.Column('type', sa.String(50), nullable=False),

        sa.Column('concentration', sa.Float()),

        sa.Column('debit', sa.Float()),

        sa.Column('pression', sa.Float()),

        sa.Column('coefficient_refroidissement', sa.Float(), nullable=False),

        sa.Column('coefficient_lubrification', sa.Float(), nullable=False),

        sa.Column('description', sa.Text()),

        sa.Column('actif', sa.Boolean(), nullable=False),

        sa.Column('date_creation', sa.DateTime())
    )


def downgrade():

    op.drop_table('lubrifiants')