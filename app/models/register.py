from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RegisterSemester(BaseModel):
    number: int
    level: int
    start: datetime
    end: datetime
    class_id: int
    unit_id: int
    current: bool
    id: int


class RegisterStudent(BaseModel):
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
    cookies: object
    semesters: list[RegisterSemester]

class RegisterSchool(BaseModel):
    name: str
    id: str
    headers: dict
    students: list[RegisterStudent]

class RegisterSymbol(BaseModel):
    name: str
    session_data: str
    schools: Optional[list[RegisterSchool]]