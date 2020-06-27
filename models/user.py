from pydantic import BaseModel
from fastapi import Query
from enum import Enum


email_regex = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"


# My Role is str type. Also the fields
class Role(str, Enum):
    admin: str = "admin"
    personel: str = "personel"


class User(BaseModel):
    name: str 
    password: str
    mail: str = Query(default=..., regex=email_regex)
    role: Role
