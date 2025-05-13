from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from core.config import settings

# Настройки
SECRET_KEY = settings.SECRET_KEY or "your-secret-key"
ALGORITHM = "HS256"
ACCESS_EXPIRE_MINUTES = 15
REFRESH_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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


def verify_token(token: str):
    """Верификация токена"""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.JWTError:
        return None