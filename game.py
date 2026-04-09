# game.py
import os
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import asyncio
from database import db

app = FastAPI()

# Подключение к БД при старте
@app.on_event("startup")
async def startup():
    await db.connect()

# ========== API ==========
@app.get('/')
async def game_page():
    with open('game.html', 'r', encoding='utf-8') as f:
        return HTMLResponse(f.read())

@app.get('/api/score')
async def save_score(
    game: str = Query(..., description="Название игры (clicker, runner, puzzle)"),
    user_id: int = Query(...),
    username: str = Query(...),
    score: int = Query(...)
):
    updated = await db.update_score(game, user_id, username, score)
    return {'ok': updated, 'new_record': updated}

@app.get('/api/top')
async def get_top(
    game: str = Query(..., description="Название игры"),
    limit: int = Query(10, ge=1, le=50)
):
    return await db.get_top(game, limit)

@app.get('/api/user_score')
async def get_user_score(
    game: str = Query(...),
    user_id: int = Query(...)
):
    score = await db.get_user_score(game, user_id)
    return {'score': score or 0}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)