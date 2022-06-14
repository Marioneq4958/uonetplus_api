from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Conference(BaseModel):
    title: str
    subject: str
    agenda: str
    present_on_conference: str
    online: Optional[str]
    id: int
    date: str
