from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from uuid import UUID
from decimal import Decimal

class StandardResponse(BaseModel):
    data: Optional[dict | list] = None
    message: str
    status: str

class RestaurantBase(BaseModel):
    name: str
    cuisine_type: Optional[str] = None
    description: Optional[str] = None
    floor_number: Optional[str] = None
    opening_time: Optional[str] = None
    closing_time: Optional[str] = None
    is_open: bool = False
    rating: Optional[Decimal] = None
    image_url: Optional[str] = None
    min_order_amount: Optional[Decimal] = None
    estimated_delivery_minutes: Optional[int] = None

class RestaurantCreate(RestaurantBase):
    pass

class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    is_open: Optional[bool] = None

class RestaurantResponse(RestaurantBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)

class MenuCategoryResponse(BaseModel):
    id: UUID
    restaurant_id: UUID
    name: str
    display_order: int
    is_active: bool
    model_config = ConfigDict(from_attributes=True)

class MenuItemResponse(BaseModel):
    id: UUID
    category_id: UUID
    restaurant_id: UUID
    name: str
    description: Optional[str] = None
    price: Decimal
    is_available: bool
    is_vegetarian: bool
    image_url: Optional[str] = None
    prep_time_minutes: Optional[int] = None
    category_name: Optional[str] = None   # from JOIN with menu_categories
    model_config = ConfigDict(from_attributes=True)
    
class MenuSearchResultResponse(MenuItemResponse):
    restaurant_name: Optional[str] = None

class AvailabilityUpdate(BaseModel):
    is_available: bool
