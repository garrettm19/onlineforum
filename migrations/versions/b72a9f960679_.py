"""empty message

Revision ID: b72a9f960679
Revises: 3747cfc9165b
Create Date: 2023-05-03 17:42:48.229383

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b72a9f960679'
down_revision = '3747cfc9165b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('timestamp', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.drop_column('timestamp')

    # ### end Alembic commands ###