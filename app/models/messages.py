from pydantic import BaseModel


class InboxMessage(BaseModel):
    id: int
    title: str
    unreaded: bool
    date: str
    sender: str
    has_attachments: bool
