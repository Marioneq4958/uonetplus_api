from pydantic import BaseModel
from typing import Optional

class Device(BaseModel):
    id: int
    name: Optional[str]
    create_date: Optional[str]

class TokenResponse(BaseModel):
    token: str
    symbol: str
    pin: str
    qr_code_image: str