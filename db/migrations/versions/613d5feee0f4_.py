"""empty message

Revision ID: 613d5feee0f4
Revises: 38dfcec22695
Create Date: 2025-03-16 14:10:22.819091

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '613d5feee0f4'
down_revision: Union[str, None] = '38dfcec22695'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('spicy_bot_history', sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('spicy_bot_history', 'updated_at')
    # ### end Alembic commands ###
