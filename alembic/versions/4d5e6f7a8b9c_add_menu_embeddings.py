"""add_menu_embeddings

Revision ID: 4d5e6f7a8b9c
Revises: 3c4d5e6f7a8b
Create Date: 2026-06-17
"""
from alembic import op
from pgvector.sqlalchemy import Vector
import sqlalchemy as sa

revision = '4d5e6f7a8b9c'
down_revision = '3c4d5e6f7a8b'
branch_labels = None
depends_on = None

EMBEDDING_DIM = 1024


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.add_column("menu_items", sa.Column("embedding", Vector(EMBEDDING_DIM), nullable=True))
    op.execute(
        "CREATE INDEX menu_items_embedding_idx ON menu_items "
        "USING hnsw (embedding vector_cosine_ops)"
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS menu_items_embedding_idx")
    op.drop_column("menu_items", "embedding")
