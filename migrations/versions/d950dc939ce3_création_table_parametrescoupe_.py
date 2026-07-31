"""Création table ParametresCoupe SessionUsinage

Revision ID: d950dc939ce3
Revises: 1814e341be0e
Create Date: 2026-07-20 15:59:34.851048

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd950dc939ce3'
down_revision = '1814e341be0e'
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        'sessions_usinage',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('date_debut', sa.DateTime(), nullable=False),
        sa.Column('date_fin', sa.DateTime(), nullable=True),
        sa.Column('date_creation', sa.DateTime(), nullable=True),

        sa.Column('outil_id', sa.Integer(), nullable=False),
        sa.Column('machine_id', sa.Integer(), nullable=False),
        sa.Column('matiere_id', sa.Integer(), nullable=False),
        sa.Column('lubrifiant_id', sa.Integer(), nullable=True),
        sa.Column('type_operation_id', sa.Integer(), nullable=False),
        sa.Column('operateur_id', sa.Integer(), nullable=False),

        sa.Column('numero_of', sa.String(length=50), nullable=True),
        sa.Column('numero_phase', sa.String(length=30), nullable=True),
        sa.Column('commentaire', sa.Text(), nullable=True),

        sa.Column('validee', sa.Boolean(), nullable=False),

        sa.Column('quantite_fabriquee', sa.Integer(), nullable=True),
        sa.Column('quantite_rebut', sa.Integer(), nullable=True),

        sa.ForeignKeyConstraint(['lubrifiant_id'], ['lubrifiants.id']),
        sa.ForeignKeyConstraint(['machine_id'], ['machines.id']),
        sa.ForeignKeyConstraint(['matiere_id'], ['matieres.id']),
        sa.ForeignKeyConstraint(['operateur_id'], ['utilisateurs.id']),
        sa.ForeignKeyConstraint(['outil_id'], ['outils.id']),
        sa.ForeignKeyConstraint(['type_operation_id'], ['types_operations.id']),

        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'parametres_coupe',

        sa.Column('id', sa.Integer(), nullable=False),

        sa.Column(
            'session_id',
            sa.Integer(),
            nullable=False
        ),

        sa.Column('vitesse_coupe', sa.Float(), nullable=True),
        sa.Column('vitesse_rotation', sa.Float(), nullable=True),
        sa.Column('avance', sa.Float(), nullable=True),
        sa.Column('avance_par_dent', sa.Float(), nullable=True),
        sa.Column('profondeur_axiale', sa.Float(), nullable=True),
        sa.Column('profondeur_radiale', sa.Float(), nullable=True),
        sa.Column('largeur_usinage', sa.Float(), nullable=True),
        sa.Column('longueur_usinage', sa.Float(), nullable=True),
        sa.Column('nombre_passes', sa.Integer(), nullable=True),
        sa.Column('temps_coupe', sa.Float(), nullable=True),
        sa.Column('engagement', sa.Float(), nullable=True),
        sa.Column('observations', sa.Text(), nullable=True),
        sa.Column('date_creation', sa.DateTime(), nullable=True),

        sa.ForeignKeyConstraint(
            ['session_id'],
            ['sessions_usinage.id']
        ),

        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('session_id')
    )


def downgrade():

    op.drop_table('parametres_coupe')
    op.drop_table('sessions_usinage')