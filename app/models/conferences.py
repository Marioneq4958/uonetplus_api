from pydantic import BaseModel
from typing import Optional


class Conference(BaseModel):
    id: int
    subject: str
    agenda: Optional[str]
    present_at_conference: str
    online: Optional[str]
    date: Optional[str]
    place: Optional[str]
