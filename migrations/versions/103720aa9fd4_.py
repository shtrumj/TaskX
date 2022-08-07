"""empty message

Revision ID: 103720aa9fd4
Revises: 8725fc5670b2
Create Date: 2022-08-02 12:03:20.072602

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '103720aa9fd4'
down_revision = '8725fc5670b2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('roleName', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_roles'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('roles')
    # ### end Alembic commands ###