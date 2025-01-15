from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel, HttpUrl
import requests
from bs4 import BeautifulSoup
from typing import List


app = FastAPI()

MARKET_INDEXES_CLASS = {
    "INDEX": "pKBk1e",
    "PERCENT_CHANGE": "JwB6zf V7hZne",
    "POINT_CHANGE": "P2Luy Ez2Ioe",
    "CURRENT_PRICE": "YMlKec",
}


class ScrapedItem(BaseModel):
    index: str
    current_price: str
    day_change_percent: str
    day_change_point: str


class ScrapedData(BaseModel):
    url: HttpUrl
    market_indexes: List[ScrapedItem]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/scrapweb", response_model=ScrapedData)
async def scrap_web(url: HttpUrl):
    try:
        page = requests.get(str(url))
        page.raise_for_status()

        soup = BeautifulSoup(page.text, "html.parser")

        extracted_data = soup.find_all("div", class_="lkR3Y")
        items = []

        for element in extracted_data:

            index_element = element.find("div", class_=MARKET_INDEXES_CLASS["INDEX"])
            index_name = index_element.get_text(strip=True) if index_element else "N/A"

            current_price_element = element.find("div", class_=MARKET_INDEXES_CLASS["CURRENT_PRICE"])
            current_price = current_price_element.get_text(strip=True) if current_price_element else "N/A"

            percent_change_element = element.find("div", class_=MARKET_INDEXES_CLASS["PERCENT_CHANGE"])
            day_change_percent = percent_change_element.get_text(strip=True) if percent_change_element else "N/A"

            point_change_element = element.find("span", class_=MARKET_INDEXES_CLASS["POINT_CHANGE"])
            day_change_point = point_change_element.get_text(strip=True) if point_change_element else "N/A"

            items.append(
                ScrapedItem(
                    index=index_name,
                    current_price=current_price,
                    day_change_percent=day_change_percent,
                    day_change_point=day_change_point,
                )
            )

        return ScrapedData(url=url, market_indexes=items)

    except Exception as e:
        return {"error": str(e)}



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)