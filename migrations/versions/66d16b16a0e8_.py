"""empty message

Revision ID: 66d16b16a0e8
Revises: 9798465ea326
Create Date: 2025-01-12 22:03:17.618459

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66d16b16a0e8'
down_revision = '9798465ea326'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('matches', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fighter_1_sig_strikes', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('fighter_2_sig_strikes', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('fighter_1_sig_strikes_pct', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('fighter_2_sig_strikes_pct', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('fighter_1_td_pct', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('fighter_2_td_pct', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('fighter_1_sub_att', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('fighter_2_sub_att', sa.Integer(), nullable=True))
        batch_op.drop_column('fighter_1_str')
        batch_op.drop_column('fighter_1_sub')
        batch_op.drop_column('fighter_2_sub')
        batch_op.drop_column('fighter_2_str')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('matches', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fighter_2_str', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('fighter_2_sub', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('fighter_1_sub', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('fighter_1_str', sa.INTEGER(), nullable=True))
        batch_op.drop_column('fighter_2_sub_att')
        batch_op.drop_column('fighter_1_sub_att')
        batch_op.drop_column('fighter_2_td_pct')
        batch_op.drop_column('fighter_1_td_pct')
        batch_op.drop_column('fighter_2_sig_strikes_pct')
        batch_op.drop_column('fighter_1_sig_strikes_pct')
        batch_op.drop_column('fighter_2_sig_strikes')
        batch_op.drop_column('fighter_1_sig_strikes')

    # ### end Alembic commands ###
