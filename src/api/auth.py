import fastapi
from fastapi import APIRouter, Depends
import fastapi.security as _security
from sqlalchemy.orm import Session

from src.api.schemas import UserCreate, User, UserEdit
from src.domain.base import get_session
from src.service import user as user_service
from src.service.exceptions import UserAlreadyExistsError, UserNotFoundError, RoleNotFoundError, BadCredentials
import jwt

from src.service.user import oauth2schema
from src.settings.config import settings

router = APIRouter()


async def get_current_user(token: str = Depends(oauth2schema), session: Session = Depends(get_session)) -> User:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        user = await user_service.get_user_by_email(session, email=payload["email"])
    except Exception as exc:
        raise fastapi.HTTPException(status_code=401, detail="Could not validate credentials") from exc

    return user


@router.post("/api/users")
async def create_user(
    user: UserCreate, session: Session = Depends(get_session)
):
    try:
        user: User = await user_service.create_user(session, user)
    except UserAlreadyExistsError as exc:
        raise fastapi.HTTPException(status_code=409, detail="Email already in use") from exc
    except RoleNotFoundError as exc:
        raise fastapi.HTTPException(status_code=404, detail="Role not found") from exc

    return await user_service.create_token(user)


@router.get("/api/users/me", response_model=User)
async def get_user(user=fastapi.Depends(get_current_user)):
    return user


@router.patch("/api/users/me")
async def edit_user(user_edit: UserEdit, session: Session = Depends(get_session), user=fastapi.Depends(get_current_user)):
    user: User = await user_service.edit_user(session, user_edit, user)
    return user


@router.post("/api/token")
async def generate_token(
    form_data: _security.OAuth2PasswordRequestForm = fastapi.Depends(),
    session: Session = Depends(get_session)
):
    try:
        user: User = await user_service.authenticate_user(session, form_data.username, form_data.password)
    except BadCredentials as exc:
        raise fastapi.HTTPException(status_code=401, detail="Invalid Credentials") from exc

    return await user_service.create_token(user)
