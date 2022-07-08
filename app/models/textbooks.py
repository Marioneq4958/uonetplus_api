from pydantic import BaseModel


class TextbooksSchoolYear(BaseModel):
    id: int
    name: str


class Textbook(BaseModel):
    id: int
    is_active: bool
    subject: str
    title: str
    description: str
    author: str
    publisher: str


class TextbooksData(BaseModel):
    is_approved: bool
    textbooks: list[Textbook]
