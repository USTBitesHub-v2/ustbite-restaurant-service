"""One-time backfill: compute embeddings for menu items seeded via Alembic data migrations.

There is no create/update-menu-item API endpoint yet, so this script is the only
way existing rows get an `embedding`. Any future create/update endpoint should
call `app.services.embeddings.embed_text` directly instead of relying on this script.

Run from the ustbite-restaurant-service directory:
    python -m scripts.backfill_menu_embeddings
"""
import asyncio
import logging

from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models.models import MenuItem, MenuCategory
from app.services.embeddings import embed_text, menu_item_blurb

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BATCH_SIZE = 20


async def backfill() -> None:
    async with AsyncSessionLocal() as db:
        stmt = (
            select(MenuItem, MenuCategory.name.label("category_name"))
            .join(MenuCategory, MenuItem.category_id == MenuCategory.id)
            .filter(MenuItem.embedding.is_(None))
        )
        rows = (await db.execute(stmt)).all()
        logger.info("Found %d menu items missing embeddings", len(rows))

        for i, (item, category_name) in enumerate(rows, start=1):
            blurb = menu_item_blurb(item.name, item.description, category_name, item.is_vegetarian)
            item.embedding = await embed_text(blurb)
            logger.info("[%d/%d] embedded %s", i, len(rows), item.name)

            if i % BATCH_SIZE == 0:
                await db.commit()

        await db.commit()
        logger.info("Backfill complete.")


if __name__ == "__main__":
    asyncio.run(backfill())
