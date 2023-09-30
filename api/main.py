from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from pymongo import MongoClient
import os


app = FastAPI()
templates = Jinja2Templates(directory="templates")

mongodb_url = os.environ['MONGODB_URL']

mongo_client = MongoClient(mongodb_url)
db = mongo_client["ragnarok"]
collection = db["monsters"]


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/monster")
async def monster(request: Request):
    return templates.TemplateResponse("monster_info.html", {"request": request})


@app.get("/api/monsters", response_model=list[dict])
async def get_monsters():
    monsters = collection.find({}, {"_id": 0, "name": 1, "id": 1})
    monsters = [monster for monster in monsters]
    return JSONResponse(content=monsters)


@app.get("/api/monster/{monster_id}")
async def get_monster(monster_id: int):
    monster = collection.find_one({"id": monster_id}, {"_id": 0})

    if monster:
        monster["image_url"] = f"https://static.divine-pride.net/images/mobs/png/{monster['id']}.png"
        return JSONResponse(content=monster)
    else:
        return JSONResponse(content={"error": f"{monster['name']} not found"}, status_code=404)
