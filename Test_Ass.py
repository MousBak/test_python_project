import aiohttp
import asyncio

async def fetch(session, url):
    # Désactiver la vérification SSL avec ssl=False
    async with session.get(url, ssl=False) as response:
        if response.status == 200:
            return await response.json()
        else:
            print(f"Erreur {response.status} pour l'URL : {url}")
            return None

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(fetch(session, url))
            tasks.append(task)
        responses = await asyncio.gather(*tasks)
        return responses

# Simuler plusieurs routes API
urls = [
    "https://jsonplaceholder.typicode.com/todos/1",
    "https://jsonplaceholder.typicode.com/todos/2"
]

# Lancer la simulation de charge
loop = asyncio.get_event_loop()
results = loop.run_until_complete(fetch_all(urls))
print(results)
