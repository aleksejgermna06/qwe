from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from apps.users.my_schema import AddPhone
from apps.users.my_service import add_phone_service
from core.models import Profile
from core.security import get_current_user
from core.database import get_async_db

session_fabrik = get_async_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/profile/add-phone", summary="Добавить номер телефона")
async def add_phone(
        phone: AddPhone,
        current_user: Profile = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)
    ):
    result = await add_phone_service(phone.telephone, current_user.id_profile, db)
    return result