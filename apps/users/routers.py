from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Profile, Token, adress
from apps.users.schema import ProfileCreate, LoginRequest, ProfileResponse, ProfileUpdate, AdressCreate, AdressResponse, AdressUpdate, LoginProfileResponse
from core.database import get_async_db
from core.security import create_tokens, pwd_context, verify_token, SECRET_KEY, ALGORITHM, get_current_user
from fastapi import Response, Request
from jose import JWTError, jwt
from typing import List
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete


router = APIRouter(prefix="/auth", tags=["auth"])
router1 = APIRouter(prefix="/user", tags=["user"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.post(
    "/register",
    response_model=ProfileResponse,
    summary="регистрация нового пользователя",
)
async def register(
    profile_data: ProfileCreate, db: AsyncSession = Depends(get_async_db)
):
    existing = await db.execute(
        select(Profile).where(Profile.mail == profile_data.mail)
    )
    if existing.scalar():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    new_profile = Profile(
        mail=profile_data.mail,
        phone=None,
        name=None,
        password=pwd_context.hash(profile_data.password),
        birthday=None,
        gender=None,
    )

    db.add(new_profile)
    await db.commit()
    await db.refresh(new_profile)
    return new_profile


@router.post("/login", response_model=ProfileResponse)
async def login(
    login_data: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_async_db),
):
    result = await db.execute(select(Profile).where(Profile.mail == login_data.mail))
    profile = result.scalar()

    if not profile or not pwd_context.verify(login_data.password, profile.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    tokens = create_tokens({"sub": str(profile.id_profile)})

    token_record = Token(
        id_profile=profile.id_profile,
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        expires_at=tokens["expires_at"],
    )

    db.add(token_record)
    await db.commit()

    response.set_cookie(
        key="access_token",
        value=tokens["access_token"],
        httponly=True,
        max_age=15 * 60,
        #secure=True,
        samesite="Lax"
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        max_age=7 * 24 * 60 * 60,
        #secure=True,
        samesite="Lax"
    )

    return LoginProfileResponse(
        id_profile=profile.id_profile,
        mail=profile.mail,
        name=profile.name,
        phone=profile.phone,
        birthday=str(profile.birthday) if profile.birthday else None,
        gender=profile.gender,
        bonus=profile.bonus
    )



@router.get(
    "/me", response_model=ProfileResponse, summary="Получение текущего пользователя"
)
async def read_me(
    request: Request,
    db: Session = Depends(get_async_db),
    profile = Depends(get_current_user)
):
    payload = request.cookies.get("access_token")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return ProfileResponse(
        id_profile=profile.id_profile,
        mail=profile.mail,
        name=profile.name,
        phone=profile.phone,
        birthday=str(profile.birthday) if profile.birthday else None,
        gender=profile.gender,
        bonus=profile.bonus
    )


@router.get("/check-token", summary="для проверки мояяя")
async def check_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="No access token")

    return {"message": "Token received", "token": token}


@router.delete("/logout", summary="Выход(удаление токена)")
async def logout(
    request: Request, response: Response, db: AsyncSession = Depends(get_async_db)
):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")

    print("Cookies in request:", request.cookies)

    if not access_token and not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No tokens found in cookies"
        )

    result = await db.execute(select(Token).where(Token.access_token == access_token))
    token_obj = result.scalar()

    if token_obj:
        await db.delete(token_obj)
        await db.commit()

    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")

    return {"message": "Logged out successfully"}


@router.get("/refresh", summary="Проверка токена")
async def refresh_tokens(
    request: Request, response: Response, db: AsyncSession = Depends(get_async_db)
):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing"
        )

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        profile_id = payload.get("sub")
        if profile_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    result = await db.execute(select(Token).where(Token.refresh_token == refresh_token))
    token_record = result.scalar()
    if not token_record:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token not found"
        )

    tokens = create_tokens({"sub": str(profile_id)})

    token_record.access_token = tokens["access_token"]
    token_record.refresh_token = tokens["refresh_token"]
    token_record.expires_at = tokens["expires_at"]

    await db.commit()

    response.set_cookie(
        key="access_token",
        value=tokens["access_token"],
        httponly=True,
        max_age=15 * 60,
        samesite="Lax",
        secure=False,
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        max_age=7 * 24 * 60 * 60,
        samesite="Lax",
        secure=False,
    )

    return {"message": "Token refreshed"}


@router1.put(
    "/profile/update", response_model=ProfileResponse, summary="Редактировать профиль"
)
async def update_profile(
    update_data: ProfileUpdate,
    current_user: Profile = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    if update_data.name is not None:
        current_user.name = update_data.name
    if update_data.phone is not None:
        current_user.phone = update_data.phone
    if update_data.birthday is not None:
        current_user.birthday = update_data.birthday
    if update_data.gender is not None:
        current_user.gender = update_data.gender

    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)

    return current_user

# @router1.post("/profile/address/add", response_model=AdressResponse, summary="Добавить адрес")
# async def add_address(
#     address_data: AdressCreate,
#     current_user: Profile = Depends(get_current_user),
#     db: AsyncSession = Depends(get_async_db)
# ):
#     new_address = adress(
#         id_profile=current_user.id_profile,
#         adress=address_data.adress
#     )
#     db.add(new_address)
#     await db.commit()
#     await db.refresh(new_address)
#     return new_address
#
# @router1.get("/profile/addresses", response_model=List[AdressResponse], summary="Получить все адреса пользователя")
# async def get_addresses(
#     current_user: Profile = Depends(get_current_user),
#     db: AsyncSession = Depends(get_async_db)
# ):
#     result = await db.execute(
#         select(adress).where(adress.id_profile == current_user.id_profile)
#     )
#     addresses = result.scalars().all()
#     return addresses










@router1.post("/profile/address/add", response_model=AdressResponse, summary="Добавить адрес")
async def add_address(
    address_data: AdressCreate,
    current_user: Profile = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    if address_data.isMain:
        await db.execute(
            update(adress)
            .where(adress.id_profile == current_user.id_profile)
            .values(is_main=False)
        )

    new_address = adress(
        id_profile=current_user.id_profile,
        settlement=address_data.settlement,
        street=address_data.street,
        entrance=address_data.entrance,
        flor=address_data.flor,
        apt_office=address_data.aptOffice,
        is_main=address_data.isMain,
    )
    db.add(new_address)
    await db.commit()
    await db.refresh(new_address)
    return AdressResponse.from_orm(new_address)

    #return new_address


@router1.get(
    "/profile/addresses",
    response_model=List[AdressResponse],
    summary="Просмотреть адреса(-> массив)",
)
async def get_addresses(
    current_user: Profile = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    result = await db.execute(
        select(adress).where(adress.id_profile == current_user.id_profile)
    )
    return result.scalars().all()


@router1.get(
    "/profile/address/main",
    response_model=List[AdressResponse],
    summary="Просмотреть основной адрес(-> массив)",
)
async def get_main_address(
    current_user: Profile = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    result = await db.execute(
        select(adress).where(
            adress.id_profile == current_user.id_profile, adress.is_main == True
        )
    )
    main_addresses = result.scalars().all()
    return main_addresses


@router1.put(
    "/profile/address/{address_id}",
    response_model=AdressResponse,
    summary="Редактировать адрес и установить его как основной",
)
async def update_address(
    address_id: int,
    address_data: AdressUpdate,
    current_user: Profile = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    result = await db.execute(
        select(adress).where(
            adress.id_adress == address_id,
            adress.id_profile == current_user.id_profile,
        )
    )
    existing = result.scalar_one_or_none()
    if not existing:
        raise HTTPException(status_code=404, detail="Адрес не найден")

    if address_data.isMain:
        await db.execute(
            update(adress)
            .where(adress.id_profile == current_user.id_profile)
            .values(is_main=False)
        )
        existing.is_main = True

    for field, value in address_data.dict(exclude_unset=True).items():
        if field == "isMain":
            continue
        setattr(existing, field if field != "aptOffice" else "apt_office", value)

    await db.commit()
    await db.refresh(existing)
    return existing


