"""Rename story to waat_words

Revision ID: 5ef2838e506e
Revises: 
Create Date: 2024-05-05 17:36:50.183689

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5ef2838e506e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.rename_table('story', 'waat_words')


def downgrade() -> None:
    op.rename_table('waat_words', 'story')
