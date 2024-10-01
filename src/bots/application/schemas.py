from pydantic import BaseModel


class SuccessAuthUserShema(BaseModel):
    id: int
    username: str
    token: str


class AuthUserShema(BaseModel):
    username: str
    password: str
