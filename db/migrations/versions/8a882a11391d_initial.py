"""Initial

Revision ID: 8a882a11391d
Revises: 
Create Date: 2024-01-31 23:25:56.421580

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a882a11391d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=32), nullable=True),
    sa.Column('balance', sa.Integer(), nullable=True),
    sa.Column('locale', sa.VARCHAR(length=2), nullable=True),
    sa.Column('role', sa.Enum('USER', 'MODERATOR', 'ADMINISTRATOR', name='role'), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('user_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###