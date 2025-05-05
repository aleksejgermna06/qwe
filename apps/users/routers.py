from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.models import Profile
from apps.users.schema import ProfileCreate, LoginRequest, TokenResponse, ProfileResponse
from core.database import get_async_db
from core.security import create_tokens, pwd_context, verify_token
from typing import Optional

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# Регистрация
@router.post("/register", response_model=ProfileResponse)
async def register(
        profile_data: ProfileCreate,
        db: AsyncSession = Depends(get_async_db)
):
    # Проверка существующего профиля
    existing = await db.execute(
        select(Profile).where(Profile.mail == profile_data.mail)
    )
    if existing.scalar():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Создание профиля
    new_profile = Profile(
        mail=profile_data.mail,
        phone=None,
        name=None,
        password=pwd_context.hash(profile_data.password),
        birthday=None,
        gender=None
    )

    db.add(new_profile)
    await db.commit()
    await db.refresh(new_profile)
    return new_profile


# Авторизация
@router.post("/login", response_model=TokenResponse)
async def login(
        login_data: LoginRequest,
        db: AsyncSession = Depends(get_async_db)
):
    result = await db.execute(
        select(Profile).where(Profile.mail == login_data.mail)
    )
    profile = result.scalar()

    if not profile or not pwd_context.verify(login_data.password, profile.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    return create_tokens({"sub": str(profile.id_profile)})


# Получение текущего пользователя
@router.get("/me", response_model=ProfileResponse)
async def read_me(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_async_db)
):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    profile = await db.execute(
        select(Profile).where(Profile.id_profile == int(payload["sub"]))
    )
    return profile.scalar_one()