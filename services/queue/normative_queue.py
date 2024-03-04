import asyncio
import aiohttp
from services.scraping.normative_scraping import get_content_from_normative

queue = asyncio.Queue()


# this method through a queue creates a list of normative urls and returns a list with structured data
async def process_queue():
    queue_normative = []
    while not queue.empty():
        get_queue = await queue.get()
        queue_normative.extend(get_queue)
    base_url = "https://www.in.gov.br/web/dou/-/"
    list_url_normative = [f'{base_url}{link}' for link in queue_normative]
    print(len(list_url_normative))
    content_normative = []

    async with aiohttp.ClientSession() as session:
        semaphore = asyncio.Semaphore(15)

        async def fetch_content(url):
            async with semaphore:
                normative = await get_content_from_normative(session, url)
                print(normative)
                content_normative.append(normative)

        await asyncio.gather(*(fetch_content(url) for url in list_url_normative))
    return content_normative
