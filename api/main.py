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
        default=None, description="monster name to search"
    ),
    page: Optional[int] = Query(
        default=None, description="page number", ge=1
    ), 
    per_page: int = Query(
        default=100, description="items per page", le=100
    ),
    
    formless: Optional[bool] = None,
    undead: Optional[bool] = None,
    brute: Optional[bool] = None,
    plant: Optional[bool] = None,
    insect: Optional[bool] = None,
    fish: Optional[bool] = None,
    demon: Optional[bool] = None,
    human: Optional[bool] = None,
    angel: Optional[bool] = None,
    dragon: Optional[bool] = None,

    neutral: Optional[bool] = None,
    water: Optional[bool] = None,
    earth: Optional[bool] = None,
    fire: Optional[bool] = None,
    wind: Optional[bool] = None,
    poison: Optional[bool] = None,
    holy: Optional[bool] = None,
    dark: Optional[bool] = None,
    ghost: Optional[bool] = None,
    maledict: Optional[bool] = None
    
):
    query = {}

    if name:
        query["name"] = {"$regex": re.escape(name), "$options": "i"}

    query_sum = []

    types_filter = []
    if formless:
        types_filter.append({"stats.race": 0})
    if undead:
        types_filter.append({"stats.race": 1})
    if brute:
        types_filter.append({"stats.race": 2})
    if plant:
        types_filter.append({"stats.race": 3})
    if insect:
        types_filter.append({"stats.race": 4})
    if fish:
        types_filter.append({"stats.race": 5})
    if demon:
        types_filter.append({"stats.race": 6})
    if human:
        types_filter.append({"stats.race": 7})
    if angel:
        types_filter.append({"stats.race": 8})
    if dragon:
        types_filter.append({"stats.race": 9})
    if types_filter:
        query_race = {}
        query_race["$or"] = types_filter
        query_sum.append(query_race)

    elements_filter = []
    if neutral:
        elements_filter.append({"stats.element": 0})
        elements_filter.append({"stats.element": 20})
        elements_filter.append({"stats.element": 40})
        elements_filter.append({"stats.element": 60})
        elements_filter.append({"stats.element": 80})
    if water:
        elements_filter.append({"stats.element": 1})
        elements_filter.append({"stats.element": 21})
        elements_filter.append({"stats.element": 41})
        elements_filter.append({"stats.element": 61})
        elements_filter.append({"stats.element": 81})
    if earth:
        elements_filter.append({"stats.element": 2})
        elements_filter.append({"stats.element": 22})
        elements_filter.append({"stats.element": 42})
        elements_filter.append({"stats.element": 62})
        elements_filter.append({"stats.element": 82})
    if fire:
        elements_filter.append({"stats.element": 3})
        elements_filter.append({"stats.element": 23})
        elements_filter.append({"stats.element": 43})
        elements_filter.append({"stats.element": 63})
        elements_filter.append({"stats.element": 83})
    if wind:
        elements_filter.append({"stats.element": 4})
        elements_filter.append({"stats.element": 24})
        elements_filter.append({"stats.element": 44})
        elements_filter.append({"stats.element": 64})
        elements_filter.append({"stats.element": 84})
    if poison:
        elements_filter.append({"stats.element": 5})
        elements_filter.append({"stats.element": 25})
        elements_filter.append({"stats.element": 45})
        elements_filter.append({"stats.element": 65})
        elements_filter.append({"stats.element": 85})
    if holy:
        elements_filter.append({"stats.element": 6})
        elements_filter.append({"stats.element": 26})
        elements_filter.append({"stats.element": 46})
        elements_filter.append({"stats.element": 66})
        elements_filter.append({"stats.element": 86})
    if dark:
        elements_filter.append({"stats.element": 7})
        elements_filter.append({"stats.element": 27})
        elements_filter.append({"stats.element": 47})
        elements_filter.append({"stats.element": 67})
        elements_filter.append({"stats.element": 87})
    if ghost:
        elements_filter.append({"stats.element": 8})
        elements_filter.append({"stats.element": 28})
        elements_filter.append({"stats.element": 48})
        elements_filter.append({"stats.element": 68})
        elements_filter.append({"stats.element": 88})
    if maledict:
        elements_filter.append({"stats.element": 9})
        elements_filter.append({"stats.element": 29})
        elements_filter.append({"stats.element": 49})
        elements_filter.append({"stats.element": 69})
        elements_filter.append({"stats.element": 89})
    if elements_filter:
        query_elements = {}
        query_elements["$or"] = elements_filter
        query_sum.append(query_elements)

    if query_sum:
        query["$and"] = query_sum

    filter_values = {
        "_id": 0,
        "name": 1,
        "id": 1,
        "stats.level": 1,
        "stats.element": 1,
        "stats.scale": 1,
        "stats.race": 1
    }

    print(query)
    
    if page is not None:
        skip = (page - 1) * per_page
        monsters = collection.find(query, filter_values).skip(skip).limit(per_page)
    else:
        monsters = collection.find(query, filter_values)
    
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
