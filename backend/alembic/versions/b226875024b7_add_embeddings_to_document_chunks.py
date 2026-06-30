"""add embeddings to document chunks

Revision ID: b226875024b7
Revises: 2cce2a019153
Create Date: 2026-06-30 18:08:33.494948

"""
from pgvector.sqlalchemy import Vector
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b226875024b7'
down_revision: Union[str, Sequence[str], None] = '2cce2a019153'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'document_chunks',
        sa.Column('embedding', Vector(384), nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('document_chunks', 'embedding')
