from pydantic import BaseModel
from typing import Optional

class GuardianContactData(BaseModel):
    home_phone: Optional[str]
    cell_phone: Optional[str]
    work_phone: Optional[str]
    email_address: Optional[str]


class StudentContactData(BaseModel):
    home_phone: Optional[str]
    cell_phone: Optional[str]
    email_address: Optional[str]


class GuardianData(BaseModel):
    id: int
    name: str
    surname: str
    kinship: Optional[str]
    address: str
    contact_data: GuardianContactData


class StudentAddressData(BaseModel):
    address: str
    registered_address: str
    correspondence_address: str


class StudentData(BaseModel):
    name: str
    second_name: Optional[str]
    surname: str
    sex: str
    brith_date: str
    brith_place: str
    family_name: Optional[str]
    polish_citizenship: int
    is_pole: bool
    address_data: StudentAddressData
    guardians: list[GuardianData]
    hide_address_data: bool
    has_pesel: bool