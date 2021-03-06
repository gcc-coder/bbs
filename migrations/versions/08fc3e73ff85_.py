"""empty message

Revision ID: 08fc3e73ff85
Revises: 
Create Date: 2020-06-23 00:07:38.942493

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '08fc3e73ff85'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cms_role',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('desc', sa.String(length=200), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('permisson', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cms_role_user',
    sa.Column('cmsrole_id', sa.Integer(), nullable=True),
    sa.Column('cmsuser_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cmsrole_id'], ['cms_role.id'], ),
    sa.ForeignKeyConstraint(['cmsuser_id'], ['cms_user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cms_role_user')
    op.drop_table('cms_role')
    # ### end Alembic commands ###
