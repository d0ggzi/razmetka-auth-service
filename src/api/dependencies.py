import fastapi
from fastapi import Depends
from sqlalchemy.orm import Session

import jwt

from src.service.user import oauth2schema
from src.settings.config import settings
from src.service import user as user_service
from src.domain.base import get_session
from src.api.schemas import User


async def get_current_user(token: str = Depends(oauth2schema), session: Session = Depends(get_session)) -> User:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        user = await user_service.get_user_by_email(session, email=payload["email"])
    except Exception as exc:
        raise fastapi.HTTPException(status_code=401, detail="Could not validate credentials") from exc

    return user
