from fastapi import APIRouter, HTTPException
from app.services import scrap_indexes
from app.models import ScrapedData

router = APIRouter()

@router.post("/", response_model=ScrapedData)
async def scrape_indexes_route(url: str):
    try:
        data = await scrap_indexes(url)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
indexes_route = router