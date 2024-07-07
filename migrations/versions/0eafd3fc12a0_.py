"""empty message

Revision ID: 0eafd3fc12a0
Revises: d9ce2a1897e5
Create Date: 2024-07-06 18:23:45.394553

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0eafd3fc12a0'
down_revision = 'd9ce2a1897e5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fullname', sa.String(length=120), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('fullname')

    # ### end Alembic commands ###