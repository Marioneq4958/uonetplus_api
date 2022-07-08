from pydantic import BaseModel

class TextbooksSchoolYear(BaseModel):
    id: int
    name: str
