import asyncio
import aiohttp
import json
import time
from services.worker.normative_worker import worker
from services.queue.normative_queue import process_queue
from services.scraping.normative_scraping import get_all_urls_pages
from services.scraping.normative_scraping import get_amount_normative
from services.scraping.normative_scraping import get_amount_pages
from create_csv import convert_json_to_csv

start_time = time.time()


async def main():
    async with aiohttp.ClientSession() as session:
        base_url = (
            'https://www.in.gov.br/consulta/-/buscar/dou?q=*&s=todos&exactDate=personalizado&'
            'sortType=0&delta=20&currentPage=1&newPage=2&score=0&id=546046623&'
            'displayDate=1709262000000&publishFrom=01-03-2024&publishTo=01-03-2024'
        )
        amount_normative = await get_amount_normative(session, base_url)
        pages = await get_amount_pages(amount_normative)
        url_pages_normative = await get_all_urls_pages(pages)
        tasks = []
        for url in url_pages_normative:
            task = asyncio.create_task(worker(session, url))
            tasks.append(task)
        await asyncio.gather(*tasks)
        content_from_normative = await process_queue()
        print(content_from_normative)

    total_execution_time = time.time() - start_time
    print(len(content_from_normative))

    json_data = json.dumps(content_from_normative, indent=2, ensure_ascii=False)

    with open('normatives.json', 'w') as json_file:
        json_file.write(json_data)

    await convert_json_to_csv('normatives.json', 'normatives.csv')

    print(f"Total execution time: {total_execution_time:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
