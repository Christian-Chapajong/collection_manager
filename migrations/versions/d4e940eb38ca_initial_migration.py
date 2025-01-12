"""Initial migration

Revision ID: d4e940eb38ca
Revises: 
Create Date: 2025-01-11 21:55:55.760187

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4e940eb38ca'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fighters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('nickname', sa.String(length=255), nullable=True),
    sa.Column('weight_class', sa.String(length=255), nullable=False),
    sa.Column('wins', sa.Integer(), nullable=True),
    sa.Column('draws', sa.Integer(), nullable=True),
    sa.Column('losses', sa.Integer(), nullable=True),
    sa.Column('height_cm', sa.Float(), nullable=True),
    sa.Column('weight_kg', sa.Float(), nullable=True),
    sa.Column('reach_cm', sa.Float(), nullable=True),
    sa.Column('stance', sa.String(length=255), nullable=True),
    sa.Column('significant_strikes_landed_per_minute', sa.Float(), nullable=True),
    sa.Column('significant_striking_accuracy', sa.Float(), nullable=True),
    sa.Column('significant_strikes_absorbed_per_minute', sa.Float(), nullable=True),
    sa.Column('significant_strike_defence', sa.Float(), nullable=True),
    sa.Column('average_takedowns_landed_per_15_minutes', sa.Float(), nullable=True),
    sa.Column('takedown_accuracy', sa.Float(), nullable=True),
    sa.Column('takedown_defense', sa.Float(), nullable=True),
    sa.Column('average_submissions_attempted_per_15_minutes', sa.Float(), nullable=True),
    sa.Column('sex', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fighters')
    # ### end Alembic commands ###
