from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Semester(BaseModel):
    number: int
    level: int
    start: datetime
    end: datetime
    class_id: int
    unit_id: int
    current: bool
    id: int

class Student(BaseModel):
    id: int
    student_id: int
    student_name: str
    student_second_name: Optional[str]
    student_surname: str
    is_register: bool
    register_id: int
    kindergarten_register_id: int
    level: int
    symbol: str
    name: Optional[str]
    year: int
    start: datetime
    end: datetime
    full_name: str
    school_id: str
    school_name: str
    school_symbol: str
    cookies: object
<<<<<<< HEAD
=======
    headers: object
>>>>>>> feature/add-mobile-access
    semesters: list
