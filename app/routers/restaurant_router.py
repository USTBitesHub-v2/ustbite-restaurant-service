from fastapi import APIRouter, Depends, HTTPException, Header, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.database import get_db
from app.schemas import StandardResponse, RestaurantResponse, RestaurantCreate, RestaurantUpdate, MenuCategoryResponse, MenuItemResponse, MenuSearchResultResponse, AvailabilityUpdate
from app.services import restaurant_service
from app.events.publisher import publish_event

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])

def format_response(data, message="Success"):
    return {"data": data, "message": message, "status": "success"}

@router.get("", response_model=StandardResponse)
async def list_restaurants(page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100), db: AsyncSession = Depends(get_db)):
    skip = (page - 1) * limit
    items = await restaurant_service.get_restaurants(db, skip=skip, limit=limit)
    data = [RestaurantResponse.model_validate(x).model_dump(mode="json") for x in items]
    return format_response(data)

@router.get("/menu/search", response_model=StandardResponse)
async def search_menu(
    query: str = Query(..., min_length=1),
    max_price: Optional[float] = Query(None, ge=0),
    vegetarian: Optional[bool] = Query(None),
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    """Cross-restaurant semantic menu search (pgvector + Titan embeddings)."""
    items = await restaurant_service.search_menu_semantic(db, query, max_price, vegetarian, limit)
    data = [MenuSearchResultResponse.model_validate(x).model_dump(mode="json") for x in items]
    return format_response(data)

@router.get("/{id}", response_model=StandardResponse)
async def get_restaurant(id: str, db: AsyncSession = Depends(get_db)):
    item = await restaurant_service.get_restaurant(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return format_response(RestaurantResponse.model_validate(item).model_dump(mode="json"))

@router.get("/{id}/menu", response_model=StandardResponse)
async def get_menu(id: str, page: int = Query(1), limit: int = Query(100), db: AsyncSession = Depends(get_db)):
    skip = (page - 1) * limit
    items = await restaurant_service.get_menu(db, id, skip=skip, limit=limit)
    data = [MenuItemResponse.model_validate(x).model_dump(mode="json") for x in items]
    return format_response(data)

@router.get("/{id}/menu/categories", response_model=StandardResponse)
async def get_categories(id: str, db: AsyncSession = Depends(get_db)):
    items = await restaurant_service.get_menu_categories(db, id)
    data = [MenuCategoryResponse.model_validate(x).model_dump(mode="json") for x in items]
    return format_response(data)

@router.post("", response_model=StandardResponse)
async def create_restaurant(payload: RestaurantCreate, db: AsyncSession = Depends(get_db), x_user_role: str = Header(None)):
    if x_user_role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    item = await restaurant_service.create_restaurant(db, payload)
    return format_response(RestaurantResponse.model_validate(item).model_dump(mode="json"), "Created successfully")

@router.put("/{id}", response_model=StandardResponse)
async def update_restaurant(id: str, payload: RestaurantUpdate, db: AsyncSession = Depends(get_db), x_user_role: str = Header(None)):
    if x_user_role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    item = await restaurant_service.update_restaurant(db, id, payload)
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    
    if payload.is_open is False:
        await publish_event("restaurant.closed", {"restaurant_id": str(item.id)})
        
    return format_response(RestaurantResponse.model_validate(item).model_dump(mode="json"))

@router.patch("/{id}/menu/items/{item_id}/availability", response_model=StandardResponse)
async def update_item_availability(id: str, item_id: str, payload: AvailabilityUpdate, db: AsyncSession = Depends(get_db)):
    item = await restaurant_service.update_item_availability(db, id, item_id, payload)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
        
    if not payload.is_available:
        await publish_event("menu.item_unavailable", {"item_id": item_id, "restaurant_id": id})
        
    return format_response(MenuItemResponse.model_validate(item).model_dump(mode="json"))
