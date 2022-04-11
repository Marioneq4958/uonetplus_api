from pydantic import BaseModel
from typing import Optional

class Login(BaseModel):
    username: str
    password: str
    symbol: str
    host: str
    ssl: Optional[bool]

class UonetPlusUczen(BaseModel):
<<<<<<< HEAD
    vulcan_cookies: object
    student: object
    school_id: str
    symbol: str
    host: str
    ssl: bool

=======
    host: str
    symbol: str
    school_id: str
    ssl: bool
    headers: object
    student: object
    vulcan_cookies: object
    payload: Optional[dict]
>>>>>>> feature/add-mobile-access
