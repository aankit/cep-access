"""dropping community district, don't know what that is

Revision ID: 0fff4c4f7863
Revises: 
Create Date: 2021-02-27 14:16:04.514968

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0fff4c4f7863'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('school',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dbn', sa.String(length=8), nullable=True),
    sa.Column('school_name', sa.String(length=100), nullable=True),
    sa.Column('school_district', sa.Integer(), nullable=True),
    sa.Column('council_district', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_school_council_district'), 'school', ['council_district'], unique=False)
    op.create_index(op.f('ix_school_dbn'), 'school', ['dbn'], unique=True)
    op.create_index(op.f('ix_school_school_district'), 'school', ['school_district'], unique=False)
    op.create_index(op.f('ix_school_school_name'), 'school', ['school_name'], unique=True)
    op.create_table('plan',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('year', sa.String(length=8), nullable=True),
    sa.Column('school_id', sa.Integer(), nullable=True),
    sa.Column('html_path', sa.String(length=250), nullable=True),
    sa.Column('pdf_path', sa.String(length=250), nullable=True),
    sa.ForeignKeyConstraint(['school_id'], ['school.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('html_path'),
    sa.UniqueConstraint('pdf_path')
    )
    op.create_index(op.f('ix_plan_year'), 'plan', ['year'], unique=False)
    op.create_table('plan_text',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('plan_id', sa.Integer(), nullable=True),
    sa.Column('page_number', sa.Integer(), nullable=True),
    sa.Column('text', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['plan_id'], ['plan.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('plan_text')
    op.drop_index(op.f('ix_plan_year'), table_name='plan')
    op.drop_table('plan')
    op.drop_index(op.f('ix_school_school_name'), table_name='school')
    op.drop_index(op.f('ix_school_school_district'), table_name='school')
    op.drop_index(op.f('ix_school_dbn'), table_name='school')
    op.drop_index(op.f('ix_school_council_district'), table_name='school')
    op.drop_table('school')
    # ### end Alembic commands ###
