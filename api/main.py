from fastapi import FastAPI, Query
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
        default=None,
        description="Monster name to search"
    ),
    page: Optional[int] = Query(
        default=1,
        description="Page number",
        ge=1
    ),
    per_page: Optional[int] = Query(
        default=60,
        description="Items per page",
        le=100
    ),
    race: Optional[str] = Query(
        default=None,
        description="Comma-separated list of races (e.g., 'undead,plant')"
    ),
    element: Optional[str] = Query(
        default=None, 
        description="Comma-separated list of elements (e.g., 'fire,dragon')"
    )
):
    query = {}

    if name:
        query["name"] = {"$regex": re.escape(name), "$options": "i"}

    # race query generate
    race_mapping = {
        "formless": 0, "undead": 1, "brute": 2, "plant": 3, "insect": 4,
        "fish": 5, "demon": 6, "human": 7, "angel": 8, "dragon": 9
    }

    if race:
        race_list = race.split(',')
        race_filters = [
            {"stats.race": race_mapping[r]}
            for r in race_list
            if r in race_mapping
        ]
        if race_filters:
            query["$or"] = race_filters

    # element query generate
    element_mapping = {
        "neutral": [0, 20, 40, 60, 80], "water": [1, 21, 41, 61, 81],
        "earth": [2, 22, 42, 62, 82], "fire": [3, 23, 43, 63, 83],
        "wind": [4, 24, 44, 64, 84], "poison": [5, 25, 45, 65, 85],
        "holy": [6, 26, 46, 66, 86], "dark": [7, 27, 47, 67, 87],
        "ghost": [8, 28, 48, 68, 88], "maledict": [9, 29, 49, 69, 89]
    }

    if element:
        element_list = element.split(',')
        element_filters = [
            {"stats.element": { "$in": element_mapping[e] }}
            for e in element_list if e in element_mapping
        ]
        if element_filters:
            if "$or" in query:
                query["$and"] = [
                    {"$or": query["$or"]}, {"$or": element_filters}
                ]
                del query["$or"]
            else:
                query["$or"] = element_filters

    # pagination
    filter_values = {
        "_id": 0,
        "name": 1,
        "id": 1,
        "stats.level": 1,
        "stats.element": 1,
        "stats.scale": 1,
        "stats.race": 1
    }

    print(query, filter_values)

    skip = (page - 1) * per_page
    monsters = collection.find(query, filter_values).skip(skip).limit(per_page)
    
    monsters = [monster for monster in monsters]
    return JSONResponse(content=monsters)


@app.get("/api/monster/{monster_id}")
async def get_monster(monster_id: int):
    monster = collection.find_one({"id": monster_id}, {"_id": 0})

    if monster:
        monster["image_url"] = f"https://static.divine-pride.net/images/mobs/png/{monster['id']}.png"
        return JSONResponse(content=monster)
    else:
        return JSONResponse(
            content={"error": f"monsterid {monster_id} not found"},
            status_code=404
        )
