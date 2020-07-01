from pydantic import BaseModel


class JwtUser(BaseModel):
    username: str
    password: str
    disable: bool = False
    role: str = None
