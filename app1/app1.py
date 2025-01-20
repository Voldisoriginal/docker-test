from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import httpx
import socket
import os

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None

items = []

@app.get("/items", response_model=List[Item])
async def get_items():
    return items

@app.post("/items", response_model=Item)
async def add_item(item: Item):
    items.append(item)
    return item

@app.get("/container_name")
async def get_container_name():
    # Получаем имя хоста (в Docker это обычно ID или имя контейнера)
    container_name = socket.gethostname()
    return {"container_name": container_name}

@app.get("/get_container_name")
async def get_container_name():
    api_url = os.getenv("API").split(',')
    results=[]
    async with httpx.AsyncClient() as client:
        for item in api_url:
            response = await client.get(f"{item}/container_name")
            results.append({"url": item, "data": response.json()})
        return {"results": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)