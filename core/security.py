from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.config import settings
from core.database import get_async_db
from core.models import Profile

# Настройки
SECRET_KEY = settings.SECRET_KEY or "your-secret-key"
ALGORITHM = "HS256"
ACCESS_EXPIRE_MINUTES = 15
REFRESH_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_current_user(
    request: Request, db: AsyncSession = Depends(get_async_db)
) -> Profile:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing access token"
        )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    result = await db.execute(select(Profile).where(Profile.id_profile == int(user_id)))
    user = result.scalar()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def create_tokens(data: dict):
    """Генерация пары токенов"""
    access_data = data.copy()
    refresh_data = data.copy()

    access_expire = datetime.utcnow() + timedelta(minutes=ACCESS_EXPIRE_MINUTES)
    refresh_expire = datetime.utcnow() + timedelta(days=REFRESH_EXPIRE_DAYS)

    access_data.update({"exp": access_expire})
    refresh_data.update({"exp": refresh_expire})

    access_token = jwt.encode(access_data, SECRET_KEY, algorithm=ALGORITHM)
    refresh_token = jwt.encode(refresh_data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_at": access_expire
    }


# def verify_token(token: str):
#     """Верификация токена"""
#     try:
#         return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#     except jwt.JWTError:
#         return None

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from datetime import datetime, timezone
from core.models import Token

def verify_token(token: str, db: Session):
    """Проверка токена: валидность + срок действия"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        access_token = token
        db_token = db.query(Token).filter(Token.access_token == access_token).first()
        if db_token is None:
            raise HTTPException(status_code=401, detail="Херня в бд не нашла беглеца}")

        if db_token.expires_at < datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="Черный мальчик просит пить")

        return payload

    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="ВСЕ ВСЕМ ПОКА ПОКА")
class Us:
    id_profile=0

async def get_current_user_prod(
    request: Request, db: AsyncSession = Depends(get_async_db)
) -> Profile:
    token = request.cookies.get("access_token")
    if not token:
        return Us

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    result = await db.execute(select(Profile).where(Profile.id_profile == int(user_id)))
    user = result.scalar()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user