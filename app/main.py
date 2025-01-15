from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel, HttpUrl
import requests
from bs4 import BeautifulSoup
from typing import List

from app.api.indexes import indexes_route

app = FastAPI()

app.include_router(indexes_route, prefix="/scrape-indexes", tags=["Scraping Indexes"])

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)