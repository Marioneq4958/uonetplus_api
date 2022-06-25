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


class Register(BaseModel):
    is_register: bool
    register_id: int
    kindergarten_register_id: int
    level: int
    symbol: str
    year: int
    start: datetime
    end: datetime
    cookies: object
    semesters: list[RegisterSemester]


class RegisterStudent(BaseModel):
    student_id: int
    student_name: str
    student_second_name: Optional[str]
    student_surname: str
    registers: Optional[list[Register]]


class RegisterSchool(BaseModel):
    name: str
    id: str
    headers: dict
    students: list[RegisterStudent]

class RegisterSymbol(BaseModel):
    name: str
    session_data: str
    schools: Optional[list[RegisterSchool]]