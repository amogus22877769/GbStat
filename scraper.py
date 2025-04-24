from aiohttp import ClientSession
import asyncio
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from os import path
from models import Base, Channel, Reflected

class Scraper:

    def __init__(self):
        self.session: ClientSession
        self.engine = create_engine('sqlite:///database.db')
        if path.isfile('database.db'):
            Reflected.prepare(self.engine)
            print('exists')
        else:
            Base.metadata.create_all(self.engine)

    async def start_session(self):
        self.session: ClientSession = ClientSession()

    async def close_session(self):
        await self.session.close()

    async def fetch(self, url: str) -> str:
        async with self.session.get(url) as response:
            return await response.text()
        
    def test(self):
        with Session(self.engine) as session:
            print(session.execute(select(Channel)).scalar().subscribers)