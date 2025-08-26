from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class OrderSummary(BaseModel):
    pricePerUnit: float
    amount: int
    orders: int

class QuickStatus(BaseModel):
    productId: str
    sellPrice: float
    buyPrice: float
    sellVolume: float
    buyVolume: int
    sellMovingWeek: int
    buyMovingWeek: int
    sellOrders: int
    buyOrders: int

class BazaarProduct(BaseModel):
    product_id: str = Field(alias="product_id")
    sell_summary: List[OrderSummary] = []
    buy_summary: List[OrderSummary] = []
    quick_status: QuickStatus

class BazaarSnapshot(BaseModel):
    products: Dict[str, BazaarProduct]
    last_updated: Optional[int] = Field(default=None, alias="lastUpdated")
    success: Optional[bool] = None
