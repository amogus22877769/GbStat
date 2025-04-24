import asyncio
from json import dump
from custom_types.info import Infos
from custom_types.target import Targets
from enums.tg import Tg
from scraper import Scraper
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from bs4.element import Tag
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from asyncio import gather, sleep
from math import ceil
from custom_types.message import MessageType
from custom_types.channel import ChannelType
from datetime import datetime
from time import strftime
from models import ChannelChange, Message, PhotoURL, VideoURL, Channel

class WebScraper(Scraper):

    def __init__(self):
        super().__init__()
        self.channels: dict[str: ChannelType] = {}
        self.messages: dict[str: list[MessageType]] = {}
        self.messages_ids: dict[str: set[MessageType['id']]] = {}

    async def get_channel_posts_count(self, username: str) -> int:
        print(f'{username=}')
        html: str = await self.fetch(Tg.URL + username)
        soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')
        self.channels[username] = {
            'username': username,
            'title': self.get(soup, 'title', 'channel'),
            'description': self.get(soup, 'description', 'channel'),
            'subscribers': self.get(soup, 'subscribers', 'channel')
        }
        self.messages_ids[username] = set()
        self.messages[username] = []
        return self.get_all(soup, 'id')[-1]
    
    async def get_channel_history(self, username: str, update: bool = False):
        channel_posts_count: int = await self.get_channel_posts_count(username)
        # if channel_posts_count > 2000:
        #     raise ValueError('too much')
        message_ids: list[int] = [channel_posts_count + 1 - i * 20 for i in range(ceil(channel_posts_count / 20))]
        await gather(*[self.get_channel_chunk_history(username, message_id) for message_id in message_ids])
        if not update:
            self.save_channel_history(username)
    
    async def get_channel_chunk_history(self, username: str, message_id: int):
        html: str = await self.fetch(f'{Tg.URL}{username}?{Tg.MESSAGE_ID_SEARCH_PARAM}={message_id}')
        soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')
        messages: set[Tag] = soup.find_all(Tg.MESSAGE.MAIN.TAG, attrs=Tg.MESSAGE.MAIN.ATTRS)
        for message in messages:
            current_message_id: int = self.get(message, 'id')
            if current_message_id not in self.messages_ids[username]:
                self.messages_ids[username].add(current_message_id)
                self.messages[username].append({
                    'id': current_message_id,
                    'caption': self.get(message, 'caption'),
                    'views': self.get(message, 'views'),
                    'datetime': self.get(message, 'datetime'),
                    'photo_urls': self.get_all(message, 'photo'),
                    'video_urls': self.get_all(message, 'video'),
                    'sticker_url': self.get(message, 'sticker'),
                })

    async def update(self, username: str):
        await self.get_channel_history(username, update=True)
        self.save_channel_history_changes(username)


    def get(self, soup: BeautifulSoup, target: str, info_type: str = 'message') -> Tag | None:
        if target.upper() not in Targets:
            raise TypeError(f'your target({target}) needs to be type Literal{Targets}')
        if info_type.upper() not in Infos:
            raise TypeError(f'your info_type needs to be type Literal{Infos}')
        attr = getattr(getattr(Tg, info_type.upper()), target.upper())
        return attr.PARSE(getattr(soup.find(attr.TAG, attrs=attr.ATTRS), attr.METHOD)(attr.ATTR)) if soup.find(attr.TAG, attrs=attr.ATTRS) else None

    def get_all(self, soup: BeautifulSoup, target: str, info_type: str = 'message') -> list[any]:
        if target.upper() not in Targets:
            raise ValueError(f'your target({target}) needs to be type Literal{Targets}')
        if info_type.upper() not in Infos:
            raise TypeError(f'your info_type needs to be type Literal{Infos}')
        attr = getattr(getattr(Tg, info_type.upper()), target.upper())
        return [attr.PARSE(getattr(tag, attr.METHOD)(attr.ATTR)) for tag in soup.find_all(attr.TAG, attrs=attr.ATTRS)]

    def save_channel_history(self, username: str) -> None:
        with Session(self.engine) as session:
            channel = self.channels[username]
            session.add(Channel(
                username=username,
                title=channel['title'],
                description=channel['description'],
                subscribers=channel['subscribers'],

            ))
            for message in self.messages[username]:
                for photo_url in message['photo_urls']:
                    session.add(PhotoURL(
                        message_id=message['id'],
                        url=photo_url,
                        type='photo_url',
                    ))
                for video_url in message['video_urls']:
                    session.add(VideoURL(
                        message_id=message['id'],
                        url = video_url,
                        type='video_url',
                    ))
                session.add(Message(
                    id_in_channel=message['id'],
                    channel_username=username,
                    caption=message['caption'],
                    views=message['views'],
                    create_date=message['datetime'],
                    sticker_url=message['sticker_url'],
                ))
            session.commit()
        self.channels[username].clear()
        self.messages[username].clear()
        self.messages_ids[username].clear()

    def save_channel_history_changes(self, username):
        with Session(self.engine) as session:
            channel = self.channels[username]
            origin_channel: Channel = session.execute(select(Channel).where(Channel.username == username)).scalar()
            changes: list[ChannelChange] = session.execute(select(ChannelChange).where(ChannelChange.username == username).order_by(desc(ChannelChange.record_date))).scalars()
            print(changes)
            est_subscribers: int = origin_channel.subscribers
            for change in changes:
                est_subscribers += change.subscribers
            if not [change for change in changes]:
                if channel['title'] != origin_channel.title or channel['description'] != origin_channel.description or channel['subscribers'] != est_subscribers:
                    print('passed')
                    session.add(ChannelChange(
                        type='channel_change',
                        channel_username=username,
                        record_date=datetime.today(),
                        title=channel['title'] if channel['title'] != origin_channel.title else None,
                        description=channel['description'] if channel['description'] != origin_channel.description else None,
                        subscribers=channel['subscribers'] if channel['subscribers'] != est_subscribers else None,
                    ))
            else:
                if channel['title'] != changes[-1].title or channel['description'] != changes[-1].description or channel['subscribers'] != est_subscribers:
                    session.add(ChannelChange(
                        channel_username=username,
                        record_date=datetime.today(),
                        title=channel['title'] if channel['title'] != changes[-1].title else None,
                        description=channel['description'] if channel['description'] != changes[-1].description else None,
                        subscribers=channel['subscribers'] if channel['subscribers'] != est_subscribers else None,
                    ))
            session.commit()

    async def start_updating_loop(self, usernames: list[str], interval: int):
        print(f'{usernames=}, {interval=}')
        while True:
            await gather(*[self.update(username) for username in usernames], sleep(interval))


if __name__ == '__main__':
    print(WebScraper().get_all(BeautifulSoup('<video src="examle1.com"></video><video src="examle2.com"></video>', 'html.parser'), 'video'))
    print(WebScraper().get_all(BeautifulSoup(
        '<i class="tgme_widget_message_sticker js-sticker_image webp_sticker_done" style="background-image: url("https://cdn4.cdn-telegram.org/file/6f3a4dc718.webp?token=PdmEMZPy-O2KVdP9XDs_ZagI9ukG3JkX5EI5EpYpb-xBMO6a-F1YjsYujVBlp3u9EUzz43pY6Z2Z0BiP8UEY0lByK0FwDAioKP-AyOVTLk5WumJhez89sKaVfAp0yiwIyCNBs1mFVfWcu8_VlSUdJNE96bLIzKJpnum3Ll0MLYjVd5Xo3RqfmdMOmRDh11KuGU47mW2ErPYxcmI3kF9bNiOCxuGsVex6n3Ksuy0Xt9cDqc-jsDE8R6Q43GgbdJXRH-AKh_9ssv6D_5_2ShcLenIiFkMUdVMo8ORUGWc3kbd64pdTMcD7h6yQA9VPyBhINHlHYnomF79I4fEn-IboGA"); width: 256px;" data-webp="https://cdn4.cdn-telegram.org/file/6f3a4dc718.webp?token=PdmEMZPy-O2KVdP9XDs_ZagI9ukG3JkX5EI5EpYpb-xBMO6a-F1YjsYujVBlp3u9EUzz43pY6Z2Z0BiP8UEY0lByK0FwDAioKP-AyOVTLk5WumJhez89sKaVfAp0yiwIyCNBs1mFVfWcu8_VlSUdJNE96bLIzKJpnum3Ll0MLYjVd5Xo3RqfmdMOmRDh11KuGU47mW2ErPYxcmI3kF9bNiOCxuGsVex6n3Ksuy0Xt9cDqc-jsDE8R6Q43GgbdJXRH-AKh_9ssv6D_5_2ShcLenIiFkMUdVMo8ORUGWc3kbd64pdTMcD7h6yQA9VPyBhINHlHYnomF79I4fEn-IboGA"><div style="padding-top:100%"></div></i>'
        , 'html.parser'), 'media'))

