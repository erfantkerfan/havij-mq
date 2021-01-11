import asyncio
import aiohttp
import tqdm
import async_timeout


async def fetch(session, url):
    with async_timeout.timeout(10, loop=session.loop):
        async with session.get(url) as response:
            return await response.text()


async def run(r):
    url = "http://localhost:8080/api/v2/user/559123"
    tasks = []
    # The default connection is only 20 - you want to stress...
    conn = aiohttp.TCPConnector(limit=20)
    tasks, responses = [], []
    async with aiohttp.ClientSession(connector=conn) as session:
        tasks = [asyncio.ensure_future(fetch(session, url)) for _ in range(r)]
        #This will show you some progress bar on the responses
        for f in tqdm.tqdm(asyncio.as_completed(tasks), total=len(tasks)):
            responses.append(await f)
    return responses

number = 10000
loop = asyncio.get_event_loop()
loop.run_until_complete(run(number))