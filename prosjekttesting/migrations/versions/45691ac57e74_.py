"""empty message

Revision ID: 45691ac57e74
Revises: 2f66bcba2a5b
Create Date: 2020-09-30 11:04:11.091368

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45691ac57e74'
down_revision = '2f66bcba2a5b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transaction', sa.Column('ammount', sa.String(length=140), nullable=True))
    op.add_column('transaction', sa.Column('receiving', sa.Integer(), nullable=True))
    op.add_column('transaction', sa.Column('sender', sa.Integer(), nullable=True))
    op.drop_constraint(None, 'transaction', type_='foreignkey')
    op.create_foreign_key(None, 'transaction', 'account', ['receiving'], ['id'])
    op.drop_column('transaction', 'user_id')
    op.drop_column('transaction', 'body')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transaction', sa.Column('body', sa.VARCHAR(length=140), nullable=True))
    op.add_column('transaction', sa.Column('user_id', sa.INTEGER(), nullable=True))
    op.drop_constraint(None, 'transaction', type_='foreignkey')
    op.create_foreign_key(None, 'transaction', 'user', ['user_id'], ['id'])
    op.drop_column('transaction', 'sender')
    op.drop_column('transaction', 'receiving')
    op.drop_column('transaction', 'ammount')
    # ### end Alembic commands ###
