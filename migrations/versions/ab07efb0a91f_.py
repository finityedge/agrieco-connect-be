"""empty message

Revision ID: ab07efb0a91f
Revises: 172067bbbf34
Create Date: 2024-07-16 19:24:33.373611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab07efb0a91f'
down_revision = '172067bbbf34'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.alter_column('start_time',
               existing_type=sa.VARCHAR(length=10),
               type_=sa.String(length=80),
               existing_nullable=False)
        batch_op.alter_column('end_time',
               existing_type=sa.VARCHAR(length=10),
               type_=sa.String(length=80),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.alter_column('end_time',
               existing_type=sa.String(length=80),
               type_=sa.VARCHAR(length=10),
               existing_nullable=False)
        batch_op.alter_column('start_time',
               existing_type=sa.String(length=80),
               type_=sa.VARCHAR(length=10),
               existing_nullable=False)

    # ### end Alembic commands ###