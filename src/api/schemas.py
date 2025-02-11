from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    name: str
    password: str
    role_name: str


class User(BaseModel):
    id: int
    email: str
    name: str
    role_name: str


class UserEdit(BaseModel):
    email: str | None = None
    name: str | None = None
    password: str | None = None
    role_name: str | None = None
