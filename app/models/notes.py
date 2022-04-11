from pydantic import BaseModel
from typing import Optional

class NotesAndAchievements(BaseModel):
    notes: list
    achievements: list

class Note(BaseModel):
    date: str
    teacher: str
    category: str
    content: str
    points: Optional[str]
    show_points: bool = False
    category_type: int = 0