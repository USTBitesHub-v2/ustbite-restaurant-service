from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.models import Restaurant, MenuCategory, MenuItem
from app.schemas import RestaurantCreate, RestaurantUpdate, AvailabilityUpdate
from app.services.embeddings import embed_text

async def get_restaurants(db: AsyncSession, skip: int = 0, limit: int = 20):
    result = await db.execute(select(Restaurant).offset(skip).limit(limit))
    return result.scalars().all()

async def get_restaurant(db: AsyncSession, restaurant_id: str):
    result = await db.execute(select(Restaurant).filter(Restaurant.id == restaurant_id))
    return result.scalars().first()

async def create_restaurant(db: AsyncSession, payload: RestaurantCreate):
    db_obj = Restaurant(**payload.model_dump())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def update_restaurant(db: AsyncSession, restaurant_id: str, payload: RestaurantUpdate):
    db_obj = await get_restaurant(db, restaurant_id)
    if not db_obj:
        return None
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(db_obj, key, value)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def get_menu(db: AsyncSession, restaurant_id: str, skip: int = 0, limit: int = 100):
    from sqlalchemy import select
    stmt = (
        select(MenuItem, MenuCategory.name.label("category_name"))
        .join(MenuCategory, MenuItem.category_id == MenuCategory.id)
        .filter(MenuItem.restaurant_id == restaurant_id)
        .offset(skip).limit(limit)
    )
    result = await db.execute(stmt)
    items = []
    for row in result.all():
        menu_item, cat_name = row[0], row[1]
        # Attach category_name dynamically — Pydantic reads it via from_attributes
        menu_item.__dict__["category_name"] = cat_name
        items.append(menu_item)
    return items

async def get_menu_categories(db: AsyncSession, restaurant_id: str):
    result = await db.execute(select(MenuCategory).filter(MenuCategory.restaurant_id == restaurant_id))
    return result.scalars().all()

async def search_menu_semantic(
    db: AsyncSession,
    query: str,
    max_price: float | None = None,
    vegetarian: bool | None = None,
    limit: int = 10,
):
    """Cross-restaurant semantic menu search via pgvector cosine distance."""
    query_embedding = await embed_text(query)

    stmt = (
        select(
            MenuItem,
            MenuCategory.name.label("category_name"),
            Restaurant.name.label("restaurant_name"),
        )
        .join(MenuCategory, MenuItem.category_id == MenuCategory.id)
        .join(Restaurant, MenuItem.restaurant_id == Restaurant.id)
        .filter(MenuItem.is_available.is_(True))
        .filter(MenuItem.embedding.is_not(None))
    )
    if max_price is not None:
        stmt = stmt.filter(MenuItem.price <= max_price)
    if vegetarian is not None:
        stmt = stmt.filter(MenuItem.is_vegetarian.is_(vegetarian))

    stmt = stmt.order_by(MenuItem.embedding.cosine_distance(query_embedding)).limit(limit)

    result = await db.execute(stmt)
    items = []
    for menu_item, category_name, restaurant_name in result.all():
        menu_item.__dict__["category_name"] = category_name
        menu_item.__dict__["restaurant_name"] = restaurant_name
        items.append(menu_item)
    return items


async def update_item_availability(db: AsyncSession, restaurant_id: str, item_id: str, payload: AvailabilityUpdate):
    result = await db.execute(select(MenuItem).filter(MenuItem.id == item_id, MenuItem.restaurant_id == restaurant_id))
    db_obj = result.scalars().first()
    if not db_obj:
        return None
    db_obj.is_available = payload.is_available
    await db.commit()
    await db.refresh(db_obj)
    return db_obj
