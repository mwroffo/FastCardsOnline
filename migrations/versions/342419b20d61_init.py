"""init

Revision ID: 342419b20d61
Revises: 
Create Date: 2018-08-19 15:01:46.657310

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '342419b20d61'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('deck',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('card',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('term', sa.String(), nullable=False),
    sa.Column('definition', sa.String(), nullable=False),
    sa.Column('deck_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['deck_id'], ['deck.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_card_definition'), 'card', ['definition'], unique=False)
    op.create_index(op.f('ix_card_term'), 'card', ['term'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_card_term'), table_name='card')
    op.drop_index(op.f('ix_card_definition'), table_name='card')
    op.drop_table('card')
    op.drop_table('deck')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###