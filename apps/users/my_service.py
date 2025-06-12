from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from core.database import get_async_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.models import AdditionalTelephone

session_fabrik = get_async_db

async def add_phone_service(phone: str, id_profile: int, session: AsyncSession):
    try:
        result = await session.execute(
            select(AdditionalTelephone).where(AdditionalTelephone.id_profile == id_profile)
        )
        existing_phones = result.scalars().all()

        if len(existing_phones) >= 10:
            raise HTTPException(status_code=400, detail="Превышен лимит дополнительных номеров")

        if any(entry.telephone == phone for entry in existing_phones):
            raise HTTPException(status_code=400, detail="Этот номер уже добавлен.")

        new_phone = AdditionalTelephone(telephone=phone, id_profile=id_profile)
        session.add(new_phone)
        await session.commit()
        return {"detail": "Номер добавлен успешно"}

    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка: {str(e)}")