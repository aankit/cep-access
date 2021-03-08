"""adding bn column to deal with old schools that no longer are in lcgms

Revision ID: e2b2ad518f47
Revises: cb39971a725a
Create Date: 2021-02-27 21:25:59.915407

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2b2ad518f47'
down_revision = 'cb39971a725a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('school', schema=None) as batch_op:
        batch_op.add_column(sa.Column('bn', sa.String(length=4), nullable=True))
        batch_op.create_index(batch_op.f('ix_school_bn'), ['bn'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('school', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_school_bn'))
        batch_op.drop_column('bn')

    # ### end Alembic commands ###