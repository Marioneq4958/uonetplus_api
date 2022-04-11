from pydantic import BaseModel

class SchoolInfo(BaseModel):
    school: object
    teachers: list

class School(BaseModel):
    name: str
    address: str
    contact: str
    headmaster: str
    pedagogue: str

class Teacher(BaseModel):
    name: str
    subject: str

