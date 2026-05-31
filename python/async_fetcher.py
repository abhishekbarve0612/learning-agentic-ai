import time
import asyncio
import httpx

from pydantic import BaseModel, ValidationError, Optional

class ContextNote(BaseModel):
    id: int
    user_id: int
    title: str
    body: Optional[str] = None

async def fetch_and_validate_notes(client: httpx.AsyncClient, note_id: int):
    url = f"https://jsonplaceholder.typicode.com/posts/{note_id}"
    
    try:
        response = await client.get(url)
        response.raise_for_status()
        raw_data = response.json()

        formatted_data = {
            "id": raw_data["id"],
            "user_id": raw_data["userId"],
            "title": raw_data["title"],
            "body": raw_data["body"]
        }

        return ContextNote(**formatted_data)

    except httpx.HTTPError as e:
        print(f"Network error on note {note_id}: {e}")
        return None
    except ValidationError as e:
        print(f"Validation error on note {note_id}: {e}")
        return None

async def process_batch_notes():
    print("Starting concurrent notes fetching...")

    async with httpx.AsyncClient() as client:
        tasks = [fetch_and_validate_notes(client, id) for id in range(1, 11)]
        results = await asyncio.gather(*tasks)

    valid_notes = [note for note in results if note is not None]

    print(f"Successfully processed {len(valid_notes)} notes.")

    for note in valid_notes:
        print(f"User ID: {note.user_id}, Title: {note.title}")

if __name__ == "__main__":
    asyncio.run(process_batch_notes())