from pydantic import BaseModel
from typing import Optional
<<<<<<< HEAD
from datetime import datetime

class NotesAndAchievements(BaseModel):
    notes: str
    achievements: str

class Note(BaseModel):
    date: datetime
=======

class NotesAndAchievements(BaseModel):
    notes: list
    achievements: list

class Note(BaseModel):
    date: str
>>>>>>> feature/add-mobile-access
    teacher: str
    category: str
    content: str
    points: Optional[str]
    show_points: bool = False
    category_type: int = 0