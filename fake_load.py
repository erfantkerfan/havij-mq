import asyncio

import aiohttp
import async_timeout
import tqdm


async def fetch(session, url):
    with async_timeout.timeout(200, loop=session.loop):
        async with session.get(url) as response:
            return await response.text()


async def run(r):
    url = "http://192.168.5.34/exam"
    # The default connection is only 20 - you want to stress...
    conn = aiohttp.TCPConnector(limit=200)
    tasks, responses = [], []
    async with aiohttp.ClientSession(connector=conn) as session:
        tasks = [asyncio.ensure_future(fetch(session, url)) for _ in range(r)]
        # This will show you some progress bar on the responses
        for f in tqdm.tqdm(asyncio.as_completed(tasks), total=len(tasks)):
            responses.append(await f)
    return responses


number = 100000
loop = asyncio.get_event_loop()
loop.run_until_complete(run(number))
