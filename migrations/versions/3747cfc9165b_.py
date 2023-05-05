"""empty message

Revision ID: 3747cfc9165b
Revises: 865c03572597
Create Date: 2023-05-02 23:12:04.922126

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3747cfc9165b'
down_revision = '865c03572597'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('threads',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('author_name', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['author_name'], ['user_info.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('author_name', sa.String(), nullable=True),
    sa.Column('thread_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_name'], ['user_info.username'], ),
    sa.ForeignKeyConstraint(['thread_id'], ['threads.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user_info', schema=None) as batch_op:
        batch_op.alter_column('username',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               existing_nullable=False)
        batch_op.alter_column('password',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_info', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               existing_nullable=True)
        batch_op.alter_column('username',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               existing_nullable=False)

    op.drop_table('comments')
    op.drop_table('threads')
    # ### end Alembic commands ###