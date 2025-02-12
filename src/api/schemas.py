import uuid
from pydantic import BaseModel, field_serializer, field_validator


class UserCreate(BaseModel):
    email: str
    name: str
    password: str
    role_name: str


class User(BaseModel):
    id: uuid.UUID
    email: str
    name: str
    role_name: str
    task_type_access: list[uuid.UUID]

    @field_serializer("id")
    def serialize_uuid(self, value):
        return str(value)

    @field_serializer("task_type_access")
    def serialize_uuid(self, value):
        return [str(v) for v in value] if value else None


class UserEdit(BaseModel):
    email: str | None = None
    name: str | None = None
    password: str | None = None
    role_name: str | None = None
    task_type_access: list[uuid.UUID] | None = None

    @field_serializer("task_type_access")
    def serialize_uuid(self, value):
        return [str(v) for v in value] if value else None

    @classmethod
    @field_validator("task_type_access", mode="before")
    def parse_uuid_list(cls, value):
        if value is None:
            return None
        if isinstance(value, list):
            return [uuid.UUID(v) for v in value]  # Преобразуем строки в UUID
        raise ValueError("task_type_access must be a list of UUID strings")
