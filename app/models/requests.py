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
    register_cookies: object
    session_data: object
    payload: Optional[dict]


class UonetPlusUzytkownik(BaseModel):
    host: str
    symbol: str
    ssl: bool
    student: object
    session_data: object
