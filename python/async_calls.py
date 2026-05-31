import time
import httpx
import asyncio

async def fetch_notes_async(client, note_id):
    url = f"https://jsonplaceholder.typicode.com/posts/{note_id}"
    response = await client.get(url)
    return response.json()

async def main():
    start_time = time.time()

    async with httpx.AsyncClient() as client:
        tasks = [fetch_notes_async(client, id) for id in range(1, 21)]

        results = await asyncio.gather(*tasks)

    print(f"Fetched {len(results)} notes in {time.time() - start_time}")

if __name__ == "__main__":
    asyncio.run(main())