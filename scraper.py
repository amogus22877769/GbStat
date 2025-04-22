from aiohttp import ClientSession
import asyncio
from sqlalchemy import create_engine

class Scraper:

    def __init__(self):
        self.session: ClientSession
        self.engine = create_engine('sqlite:///database.db')

    async def start_session(self):
        self.session: ClientSession = ClientSession()

    async def close_session(self):
        await self.session.close()

    async def fetch(self, url: str) -> str:
        async with self.session.get(url) as response:
            return await response.text()