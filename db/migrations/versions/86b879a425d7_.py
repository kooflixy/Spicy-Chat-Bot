"""empty message

Revision ID: 86b879a425d7
Revises: 729246b92748
Create Date: 2025-03-11 20:41:45.620760

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86b879a425d7'
down_revision: Union[str, None] = '729246b92748'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'id',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger(),
               existing_nullable=False,
               autoincrement=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'id',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER(),
               existing_nullable=False,
               autoincrement=True)
    # ### end Alembic commands ###
