from pydantic import BaseModel
from typing import Optional


class Login(BaseModel):
    username: str
    password: str
    host: str
    ssl: Optional[bool]


class UonetPlusUczen(BaseModel):
    host: str
    symbol: str
    school_id: str
    ssl: bool
    headers: object
    student: object
    session_data: object
    payload: Optional[dict]
