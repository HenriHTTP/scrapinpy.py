from services.scraping.normative_scraping import get_url_normative
from services.queue.normative_queue import queue


# this method execute the method for structure normative and append to queue
async def worker(session, url):
    all_normative = await get_url_normative(session, url)
    await queue.put(all_normative)
