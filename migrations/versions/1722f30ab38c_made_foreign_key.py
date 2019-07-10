"""Made foreign key


Revision ID: 1722f30ab38c
Revises: 71084cc3475d
Create Date: 2019-07-07 22:21:06.840395

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1722f30ab38c'
down_revision = '71084cc3475d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('clients', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('projects', 'client_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('projects', 'client_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('clients', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
