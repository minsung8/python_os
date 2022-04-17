from re import L
import time
import asyncio
import aiohttp

async def request_site(session, url):

    async with session.get(url) as response:
        print('read content {0}, from {1}'.format(response.content_length, url))

async def request_all_sites(urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(request_site(session, url))
            tasks.append(task)

        await asyncio.gather(*tasks, return_exceptions=True)

def main():
    urls = [
        'https://www.jython.org',
        'http://olympus.realpython.org/dice',
        'https://realpython.com'
    ] * 50

    start_time = time.time()

    asyncio.run(request_all_sites(urls))
    #asyncio.get_event_loop().run_until_complete(request_all_sites(urls))

    duration = time.time() - start_time

    print(f'asyncio Download {len(urls)} sites in {duration} seconds')

if __name__ == '__main__':
    main()

# 21s
