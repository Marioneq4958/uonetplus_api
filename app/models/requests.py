from pydantic import BaseModel
from typing import Optional

class Login(BaseModel):
    username: str
    password: str
    symbol: str
    host: str
    ssl: Optional[bool]

class UonetPlusUczen(BaseModel):
    vulcan_cookies: object
    student: object
    school_id: str
    symbol: str
    host: str
    ssl: bool

