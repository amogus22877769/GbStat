import aiohttp
from bs4 import BeautifulSoup
import asyncio

class DotaTrackerApi:
    async def get_match_links(self, url) -> list[str]:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                # print(soup)
                tags = soup.find_all('a', title='View Match on Stratz.com')
                return list(map(lambda tag: tag['href'], tags))

DotaTrackerApi = DotaTrackerApi()
print(asyncio.run(DotaTrackerApi.get_match_links('https://dota2protracker.com/tournaments')))
# print(requests.get('https://dota2protracker.com/tournaments').text)