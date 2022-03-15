from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotesAndAchievements(BaseModel):
    notes: str
    achievements: str

class Note(BaseModel):
    date: datetime
    teacher: str
    category: str
    content: str
    points: Optional[str]
    show_points: bool = False
    category_type: int = 0