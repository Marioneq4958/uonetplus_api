from pydantic import BaseModel
from typing import Optional

class Login(BaseModel):
    username: str
    password: str
    symbol: str
    host: str
    ssl: Optional[bool]

class UonetPlusUczen(BaseModel):
    host: str
    symbol: str
    school_id: str
    ssl: bool
    headers: object
    student: object
    vulcan_cookies: object
    payload: Optional[dict]
