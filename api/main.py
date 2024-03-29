from fastapi import FastAPI, Request, Query
from typing import List, Optional
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from pymongo import MongoClient
import os
import re


app = FastAPI()
templates = Jinja2Templates(directory="templates")

mongodb_url = os.getenv(
    'MONGODB_URL',
    'mongodb://root:changeme@localhost:27017/'
)

mongo_client = MongoClient(mongodb_url)
db = mongo_client["ragnarok"]
collection = db["monsters"]


@app.get("/api/health")
async def healthz():
    status = { "healthy": "true" }
    return JSONResponse(content=status)


@app.get("/api/monsters", response_model=List[dict])
async def get_monsters(
    name: Optional[str] = Query(
        default=None, description="Monster name to search"
    ),
    page: Optional[int] = Query(
        default=None, description="Page number", ge=1
    ), 
    per_page: int = Query(
        default=100, description="Items per page", le=100
    )
):
    query = {}

    if name:
        query["name"] = {"$regex": re.escape(name), "$options": "i"}

    if page is None:
        monsters = collection.find(query, {"_id": 0, "name": 1, "id": 1})
    else:
        skip = (page - 1) * per_page
        monsters = collection.find(query, {
            "_id": 0,
            "name": 1,
            "id": 1,
            "stats.level": 1,
            "stats.element": 1,
            "stats.scale": 1,
            "stats.race": 1
        }).skip(skip).limit(per_page)
    
    monsters = [monster for monster in monsters]
    return JSONResponse(content=monsters)


@app.get("/api/monster/{monster_id}")
async def get_monster(monster_id: int):
    monster = collection.find_one({"id": monster_id}, {"_id": 0})

    if monster:
        monster["image_url"] = f"https://static.divine-pride.net/images/mobs/png/{monster['id']}.png"
        return JSONResponse(content=monster)
    else:
        return JSONResponse(content={"error": f"monsterid {monster_id} not found"}, status_code=404)
