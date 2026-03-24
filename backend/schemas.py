from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class InventoryItemBase(BaseModel):
    product_name: str
    wholesale_cost: float
    desired_margin_percent: float
    current_retail_price: float
    is_active: bool = True

class InventoryItemCreate(InventoryItemBase):
    pass

class InventoryItem(InventoryItemBase):
    id: int
    tenant_id: int

    class Config:
        from_attributes = True

class TenantBase(BaseModel):
    name: str
    contact_number: str

class TenantCreate(TenantBase):
    pass

class Tenant(TenantBase):
    id: int
    created_at: datetime
    inventory: List[InventoryItem] = []

    class Config:
        from_attributes = True
