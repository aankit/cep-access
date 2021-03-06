"""dropping unique school name because of PS 253

Revision ID: cb39971a725a
Revises: 4320cb091f28
Create Date: 2021-02-27 20:30:54.223814

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb39971a725a'
down_revision = '4320cb091f28'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('school', schema=None) as batch_op:
        batch_op.drop_index('ix_school_school_name')
        batch_op.create_index(batch_op.f('ix_school_school_name'), ['school_name'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('school', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_school_school_name'))
        batch_op.create_index('ix_school_school_name', ['school_name'], unique=1)

    # ### end Alembic commands ###
