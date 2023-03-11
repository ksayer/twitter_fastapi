"""like

Revision ID: c2cf0d3ec332
Revises: 2d33c5bdfad7
Create Date: 2023-03-11 23:00:42.573947

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2cf0d3ec332'
down_revision = '2d33c5bdfad7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('like',
    sa.Column('twit_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['twit_id'], ['twit.tweet_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('twit_id', 'user_id')
    )
    op.create_index(op.f('ix_like_twit_id'), 'like', ['twit_id'], unique=False)
    op.create_index(op.f('ix_like_user_id'), 'like', ['user_id'], unique=False)
    op.create_unique_constraint(None, 'twit', ['tweet_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'twit', type_='unique')
    op.drop_index(op.f('ix_like_user_id'), table_name='like')
    op.drop_index(op.f('ix_like_twit_id'), table_name='like')
    op.drop_table('like')
    # ### end Alembic commands ###
