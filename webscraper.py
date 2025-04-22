from enums.tg import Tg
from scraper import Scraper
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from bs4.element import Tag
import sqlalchemy
from asyncio import gather
from math import ceil
from custom_types.message import Message

class WebScraper(Scraper):

    messages: list[Message]
    messages_ids: set[Message['id']]

    async def get_channel_posts_count(self, username: str) -> int:
        html: str = await self.fetch(Tg.URL + username)
        soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')
        last_message_link: set[Tag] = soup.find_all(Tg.MESSAGE.LINK.TAG, attrs=Tg.MESSAGE.LINK.ATTRS)[-1]
        return int(last_message_link[Tg.MESSAGE.LINK.LINK_ATTR].split('/')[1])
    
    async def get_channel_history(self, username: str):
        channel_posts_count: int = await self.get_channel_posts_count(username)
        if channel_posts_count > 2000:
            return 'currently not supporting'
        message_ids: list[int] = [10 + i * 20 for i in range(ceil(channel_posts_count / 20))]
        await gather(*[self.get_channel_chunk_history(username, message_id) for message_id in message_ids])
    
    async def get_channel_chunk_history(self, username: str, message_id: int):
        html: str = await self.fetch(f'{Tg.URL}{username}?{Tg.MESSAGE_ID_SEARCH_PARAM}={message_id}')
        soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')
        messages: set[Tag] = soup.find_all(Tg.MESSAGE.MAIN.TAG, attrs=Tg.MESSAGE.MAIN.ATTRS)
        for message in messages:
            link: Tag = message.find(Tg.MESSAGE.LINK.TAG, attrs=Tg.MESSAGE.LINK.ATTRS)
            current_message_id: int = int(link[Tg.MESSAGE.LINK.LINK_ATTR].split('/')[1])
            if current_message_id not in self.messages_ids:
                




                



    async def test_dom(self, usernames: list[str]) -> list[int]:
        session: ClientSession = ClientSession()
        for username in usernames:
            channel_main_page = session.get('https:/t.me/s/username')
            soup = BeautifulSoup(channel_main_page.text, "html.parser")
            last_message_id: int = int(soup.find_all('div', class_='tgme_widget_message text_not_supported_wrap js-widget_message')[-1]['data-post'].slice('/')[1])
            channel_page = session.get(f'https:/t.me/s/username/?before={last_message_id}')





