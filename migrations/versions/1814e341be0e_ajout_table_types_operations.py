"""Ajout table types_operations

Revision ID: 1814e341be0e
Revises: c93616b8aab8
Create Date: 2026-07-17 19:02:46.973526
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1814e341be0e'
down_revision = 'c93616b8aab8'
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        'types_operations',

        sa.Column('id', sa.Integer(), primary_key=True),

        sa.Column(
            'nom',
            sa.Enum(
                'FRAISAGE',
                'SURFACAGE',
                'CONTOURNAGE',
                'RAINURAGE',
                'PERCAGE',
                'ALESAGE',
                'TARAUDAGE',
                'FILETAGE',
                'POINTAGE',
                'CHANFREINAGE',
                'LAMAGE',
                'POCHE',
                'AUTRE',
                name='nomoperation'
            ),
            nullable=False,
            unique=True
        ),

        sa.Column('description', sa.Text()),

        sa.Column('actif', sa.Boolean(), nullable=False)
    )


def downgrade():

    op.drop_table('types_operations')