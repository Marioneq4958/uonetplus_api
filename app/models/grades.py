from pydantic import BaseModel
from typing import Optional

class Grades(BaseModel):
    is_average: bool
    is_points: bool
    subjects: list
    descriptive_grades: list

class Subject(BaseModel):
    name: str
    visible_subject: bool
    position: int
    average: float
    proposed_grade: Optional[str]
    fianl_grade: Optional[str]
    proposed_points: Optional[str]
    final_points: Optional[str]
    grades: list

class Grade(BaseModel):
    entry: str
    color: str
    symbol: Optional[str]
    description: Optional[str]
    weight_value: float
    date: str
    teacher: str

class DescriptiveGrade(BaseModel):
    subject: str
    description: str
    is_religia_or_etyka: bool

