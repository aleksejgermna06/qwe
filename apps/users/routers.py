from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.models import Profile, Token
from apps.users.schema import ProfileCreate, LoginRequest, TokenResponse, ProfileResponse
from core.database import get_async_db
from core.security import create_tokens, pwd_context, verify_token
from typing import Optional
from apps.users.token_service import create_token_record
from datetime import datetime, timedelta

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# Регистрация
@router.post("/register", response_model=ProfileResponse)
async def register(
        profile_data: ProfileCreate,
        db: AsyncSession = Depends(get_async_db)
):
    existing = await db.execute(
        select(Profile).where(Profile.mail == profile_data.mail)
    )
    if existing.scalar():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

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
    # tokens = create_tokens(new_user.id)    ЕСЛИ НУЖНА АВТОРИЗАЦИЯ СРАЗУ ПОСЛЕ РЕГИСТРАЦИИ
    # await create_token_record(db, new_user.id, tokens)
    #
    # return TokenResponse(**tokens)

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


    tokens = create_tokens({"sub": str(profile.id_profile)})

    token_record = Token(
        id_profile=profile.id_profile,
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        expires_at=datetime.utcnow() + timedelta(minutes=30)
    )

    db.add(token_record)
    await db.commit()

    return tokens

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