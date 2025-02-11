import fastapi.security as _security

from src.domain.database import db, ResourceNotFound, ResourceAlreadyExist
import src.api.schemas as schemas
import jwt

from src.service.exceptions import UserAlreadyExistsError, UserNotFoundError, RoleNotFoundError
from src.settings.config import settings

oauth2schema = _security.OAuth2PasswordBearer(tokenUrl="/api/token")


async def get_user_by_email(email: str) -> schemas.User:
    try:
        db_id, db_email, name, role_name = db.get_user(email)
    except ResourceNotFound as exc:
        raise UserNotFoundError from exc
    user = schemas.User(id=db_id, email=db_email, name=name, role_name=role_name)
    return user


async def edit_user(user_edit: schemas.UserEdit, user: schemas.User) -> schemas.User:
    # todo:
    if user_edit.name is not None:
        ...
    if user_edit.email is not None:
        ...
    if user_edit.password is not None:
        ...
    if user_edit.role_name is not None:
        ...
    user_res = schemas.User(id=user.id, email=user_edit.email, name=user_edit.name)
    return user_res


async def create_user(user: schemas.UserCreate):
    try:
        user_id = db.reg_user(email=user.email, password=user.password, name=user.name, role_name=user.role_name)
    except ResourceAlreadyExist as exc:
        raise UserAlreadyExistsError from exc
    except ResourceNotFound as exc:
        raise RoleNotFoundError from exc

    user_res = schemas.User(id=user_id, email=user.email, name=user.name, role_name=user.role_name)
    return user_res


async def authenticate_user(email: str, password: str) -> schemas.User | bool:
    user = await get_user_by_email(email)
    try:
        db.login(email, password)
    except ResourceNotFound:
        raise UserNotFoundError

    return user


async def create_token(user: schemas.User):
    token = jwt.encode(user.dict(), settings.JWT_SECRET)

    return dict(access_token=token, token_type="bearer")
