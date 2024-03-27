"""added work and supply tables

Revision ID: 6040e6a7be5b
Revises: d1c5aa9b4ecc
Create Date: 2024-03-26 21:08:41.045901

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6040e6a7be5b'
down_revision: Union[str, None] = 'd1c5aa9b4ecc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('supply',
    sa.Column('title', sa.String(length=70), nullable=False),
    sa.Column('supply_type', sa.String(length=50), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('title')
    )
    op.create_table('work',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('title', sa.String(length=70), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('duration_in_minutes', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('work')
    op.drop_table('supply')
    # ### end Alembic commands ###