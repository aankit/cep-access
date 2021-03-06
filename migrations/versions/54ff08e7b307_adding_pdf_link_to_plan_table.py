"""adding pdf link to plan table

Revision ID: 54ff08e7b307
Revises: df3fd30ef0fb
Create Date: 2021-03-28 15:42:37.501974

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54ff08e7b307'
down_revision = 'df3fd30ef0fb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('plan', schema=None) as batch_op:
        batch_op.add_column(sa.Column('pdf_link', sa.String(length=100), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('plan', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('pdf_link')

    # ### end Alembic commands ###
