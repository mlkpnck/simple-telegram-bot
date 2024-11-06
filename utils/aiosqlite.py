import asyncio, aiosqlite
import datetime


class DatabaseBot:

    def __init__(self, db_file):
        self.db_file = db_file
        self.lock = asyncio.Lock()

    async def __aenter__(self):
        self.db = await aiosqlite.connect(self.db_file)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.db.close()

    async def create_table(self):
        async with self.lock:
            async with self.db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY,telegram_id INTEGER NOT NULL,date INTEGER NOT NULL )",):
                return await self.db.commit()

    async def set_username(self, telegram_id: int, username: str):
        async with self.lock:
            async with self.db.execute("UPDATE users SET username = ? WHERE telegram_id = ?",
                                       (telegram_id, username)):
                return await self.db.commit()

    async def reg_user(self, telegram_id: int):
        async with self.lock:
            async with self.db.execute("INSERT INTO users (telegram_id) VALUES (?)",(telegram_id)):
                return await self.db.commit()

    async def get_user(self, telegram_id: int):
        async with self.lock:
            async with self.db.execute("SELECT telegram_id FROM users WHERE telegram_id = ?", (telegram_id,)) as cursor:
                user_exist = await cursor.fetchone()
                return user_exist

    async def check_user(self, telegram_id: int):
        async with self.lock:
            async with self.db.execute("SELECT telegram_id FROM users WHERE telegram_id = ?", (telegram_id,)) as cursor:
                user_exist = await cursor.fetchone()
                return bool(user_exist)