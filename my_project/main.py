from fastapi import FastAPI
from typing import List
from . import crud, schemas

app = FastAPI(title="Telegram Analytics API")

@app.get("/api/reports/top-products", response_model=List[schemas.ProductReport])
def top_products(limit: int = 10):
    return crud.get_top_products(limit)

@app.get("/api/channels/{channel_name}/activity", response_model=List[schemas.ChannelActivity])
def channel_activity(channel_name: str):
    return crud.get_channel_activity(channel_name)

@app.get("/api/search/messages", response_model=List[schemas.MessageSearchResult])
def search_messages(query: str):
    return crud.search_messages(query)

@app.get("/api/search/messages")
def search_endpoint(query: str):
    results = search_messages(query)
    return results
