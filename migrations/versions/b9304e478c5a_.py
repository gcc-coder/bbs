"""empty message

Revision ID: b9304e478c5a
Revises: 08fc3e73ff85
Create Date: 2020-06-25 18:29:13.378692

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b9304e478c5a'
down_revision = '08fc3e73ff85'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cms_role', sa.Column('permission', sa.Integer(), nullable=True))
    op.drop_column('cms_role', 'permisson')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cms_role', sa.Column('permisson', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_column('cms_role', 'permission')
    # ### end Alembic commands ###