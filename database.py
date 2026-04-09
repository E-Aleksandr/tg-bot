# database.py
import os
import asyncpg
from typing import List, Dict, Optional

DATABASE_URL = os.environ.get("DATABASE_URL")  # Railway даст эту переменную

class Database:
    def __init__(self):
        self.pool = None
    
    async def connect(self):
        self.pool = await asyncpg.create_pool(DATABASE_URL)
        await self.init_tables()
    
    async def init_tables(self):
        async with self.pool.acquire() as conn:
            # Таблица игр
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS games (
                    game_id SERIAL PRIMARY KEY,
                    game_name TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            ''')
            
            # Таблица рекордов
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS scores (
                    score_id SERIAL PRIMARY KEY,
                    game_id INT REFERENCES games(game_id) ON DELETE CASCADE,
                    user_id BIGINT NOT NULL,
                    username TEXT,
                    score INT NOT NULL,
                    created_at TIMESTAMP DEFAULT NOW(),
                    UNIQUE(game_id, user_id)
                )
            ''')
            
            # Индексы
            await conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_scores_game_score 
                ON scores(game_id, score DESC)
            ''')
    
    async def get_or_create_game(self, game_name: str) -> int:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                'INSERT INTO games (game_name) VALUES ($1) ON CONFLICT (game_name) DO UPDATE SET game_name = EXCLUDED.game_name RETURNING game_id',
                game_name
            )
            return row['game_id']
    
    async def update_score(self, game_name: str, user_id: int, username: str, score: int) -> bool:
        game_id = await self.get_or_create_game(game_name)
        
        async with self.pool.acquire() as conn:
            # Получаем текущий рекорд
            current = await conn.fetchrow(
                'SELECT score FROM scores WHERE game_id = $1 AND user_id = $2',
                game_id, user_id
            )
            
            if current and score <= current['score']:
                return False  # не побил рекорд
            
            # Сохраняем новый рекорд
            await conn.execute('''
                INSERT INTO scores (game_id, user_id, username, score)
                VALUES ($1, $2, $3, $4)
                ON CONFLICT (game_id, user_id)
                DO UPDATE SET score = EXCLUDED.score, created_at = NOW()
            ''', game_id, user_id, username, score)
            return True
    
    async def get_top(self, game_name: str, limit: int = 10) -> List[Dict]:
        game_id = await self.get_or_create_game(game_name)
        
        async with self.pool.acquire() as conn:
            rows = await conn.fetch('''
                SELECT username, score FROM scores
                WHERE game_id = $1
                ORDER BY score DESC
                LIMIT $2
            ''', game_id, limit)
            return [{'username': r['username'], 'score': r['score']} for r in rows]
    
    async def get_user_score(self, game_name: str, user_id: int) -> Optional[int]:
        game_id = await self.get_or_create_game(game_name)
        
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                'SELECT score FROM scores WHERE game_id = $1 AND user_id = $2',
                game_id, user_id
            )
            return row['score'] if row else None

db = Database()