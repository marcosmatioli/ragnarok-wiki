from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import httpx
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class MonsterInfo(BaseModel):
    id: int
    name: str
    health: int

async def fetch_monster_data(monster_id):
    url = f"https://www.divine-pride.net/api/database/Monster/{monster_id}?apiKey=d8a0fbd9a7f4dfd9d330170bcfb2bfee"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            monster_data = response.json()
            return monster_data
        else:
            return None

@app.get("/monster/{monster_id}")
async def read_item(request: Request, monster_id: int):
    monster_data = await fetch_monster_data(monster_id)
    if monster_data:
        monster_info = MonsterInfo(id=monster_data["id"], name=monster_data["name"], health=monster_data["stats"]["health"])
    else:
        monster_info = MonsterInfo(name="Monster Not Found", health=0)
    return templates.TemplateResponse("monster_info.html", {"request": request, "monster_info": monster_info})

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/data")
async def get_data():
    try:
        with open("templates/data.json", "r") as file:
            data = json.load(file)
        return JSONResponse(content=data)
    except FileNotFoundError:
        return JSONResponse(content={"error": "Arquivo não encontrado"}, status_code=404)
