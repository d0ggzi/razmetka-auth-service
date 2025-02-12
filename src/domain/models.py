from uuid import UUID

import uuid
from sqlalchemy import Uuid, String, ForeignKey
from sqlalchemy import Column
from sqlalchemy.orm import relationship

from src.domain.base import BaseModel


class Role(BaseModel):
    __tablename__ = "role"

    uuid: UUID = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    name: str = Column(String(255), nullable=False)
    user = relationship("User", back_populates="role")


class User(BaseModel):
    __tablename__ = "users"

    uuid: UUID = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    name: str = Column(String(255), nullable=False)
    email: str = Column(String(255), nullable=False, unique=True)
    password: str = Column(String(255), nullable=False)
    role_id: UUID = Column(Uuid(as_uuid=True), ForeignKey("role.uuid"), primary_key=True)

    role = relationship("Role", back_populates="user")
    task_access = relationship(
        "UserTaskTypeAccess",
        back_populates="user",
    )


class UserTaskTypeAccess(BaseModel):
    __tablename__ = "user_task_type_access"

    user_id: UUID = Column(Uuid(as_uuid=True), ForeignKey("users.uuid"), primary_key=True)
    task_type_id: UUID = Column(Uuid(as_uuid=True), nullable=False, primary_key=True)

    user = relationship("User", back_populates="task_access")
