from pydantic import BaseModel, HttpUrl
from typing import List 

class IndexItem(BaseModel):
    index: str
    current_price: str
    day_change_percent: str
    day_change_point: str

class ScrapedData(BaseModel):
    url: HttpUrl
    market_indexes: List[IndexItem]


