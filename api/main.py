from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from database.engine_db import AsyncSessionLocal
from database.crud import get_photo_urls_by_search_uuid

from uuid import UUID

app = FastAPI()

templates = Jinja2Templates(directory="api/templates")
app.mount("/static", StaticFiles(directory="api/static"), name="static")

@app.get("/search/{search_uuid}")
async def show_search_results(search_uuid: UUID, request: Request):
    """
    Возвращает страницу с фото, соответствующими поиску по search_uuid.
    """
    async with AsyncSessionLocal() as session:
        photo_urls = await get_photo_urls_by_search_uuid(search_uuid, session)
    
    if photo_urls and isinstance(photo_urls[0], list):
        photo_urls = photo_urls[0]
    
    if not photo_urls:
        raise HTTPException(status_code=404, detail="Search not found")

    print(isinstance(photo_urls, list), photo_urls)
    
    return templates.TemplateResponse("result.html", {"request": request, "photo_urls": photo_urls})
