from pydantic import BaseModel, Field

class Note(BaseModel):
    id: str
    title: str
    content: str = Field(..., max_length=250)
    is_archived: bool = False

raw_api_response = {
    "id": "101",
    "title": "Team standup notes",
    "content": "Discussion included project timelines and deliverables.",
    "is_archived": False
}

validated_notes = Note(**raw_api_response)

print(validated_notes.id)

print(validated_notes.is_archived)

print(validated_notes.content)

print(validated_notes.title)