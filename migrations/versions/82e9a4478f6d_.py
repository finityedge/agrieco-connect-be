"""empty message

Revision ID: 82e9a4478f6d
Revises: c8284173907c
Create Date: 2024-07-24 22:20:17.842531

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82e9a4478f6d'
down_revision = 'c8284173907c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('appointment_availabilities', schema=None) as batch_op:
        batch_op.add_column(sa.Column('availability_slot_start', sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column('availability_slot_end', sa.DateTime(), nullable=False))
        batch_op.drop_column('availability_time')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('appointment_availabilities', schema=None) as batch_op:
        batch_op.add_column(sa.Column('availability_time', sa.VARCHAR(length=80), autoincrement=False, nullable=False))
        batch_op.drop_column('availability_slot_end')
        batch_op.drop_column('availability_slot_start')

    # ### end Alembic commands ###
