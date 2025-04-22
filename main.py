import asyncio
from webscraper import WebScraper


# async def get_channel_info(username: str, link: str | None = None, messages: list[int] | None = None):
#     session: aiohttp.ClientSession = aiohttp.ClientSession()
#     response = await session.get(f'https://t.me{link if link else f'/s/{username}'}')
#     soup = BeautifulSoup(await response.text(), "html.parser")
#     await session.close()
#     views = [{
#         'view': div.find_all('span', class_='tgme_widget_message_views')[0].text if div.find_all('span',
#                                                                                                  class_='tgme_widget_message_views') else 'service message',
#         'datetime': div.a.time['datetime'],
#     } for div in soup.find_all('div', class_='tgme_widget_message_info short js-message_info')]
#     print("robotoet")
#     if not soup.find_all('link', rel='prev'):
#         return list(reversed([*views, *messages]))
#     return await get_channel_info(username, link=soup.find('link', rel='prev')['href'], messages=[*views, *messages])


# messages = asyncio.run(get_channel_info('cheloveckClash', messages=[]))

# with open('messages.json', 'w') as f:
#     json.dump(messages, f, indent=2)
# f.close()

# x = list(range(1, len(messages) + 1))
# y = [m['view'] if m['view'] != 'service message' else 0 for m in reversed(messages)]
# plt.scatter(x, y)
# plt.show()

async def main():
    web_scraper: WebScraper = WebScraper()
    await web_scraper.start_session()
    await web_scraper.get_channel_history('amogus22877769')
    await web_scraper.close_session()

if __name__ == '__main__':
    asyncio.run(main())
