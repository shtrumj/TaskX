"""empty message

Revision ID: 8725fc5670b2
Revises: 338c766cdd14
Create Date: 2022-08-01 16:37:33.400300

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8725fc5670b2'
down_revision = '338c766cdd14'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('servers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('remarks', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('hyper_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('fk_servers_hyperid_hypervisor', type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('fk_servers_hyper_id_hypervisor'), 'hypervisor', ['hyper_id'], ['id'])
        batch_op.drop_column('hyperid')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('servers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('hyperid', sa.INTEGER(), nullable=True))
        batch_op.drop_constraint(batch_op.f('fk_servers_hyper_id_hypervisor'), type_='foreignkey')
        batch_op.create_foreign_key('fk_servers_hyperid_hypervisor', 'hypervisor', ['hyperid'], ['id'])
        batch_op.drop_column('hyper_id')
        batch_op.drop_column('remarks')

    # ### end Alembic commands ###