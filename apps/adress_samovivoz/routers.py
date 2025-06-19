from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
#from apps.adress_samovivoz.models import AdressSamovivoz
from core.models import AdressSamovivoz
from apps.adress_samovivoz.schema import AdressIn, AdressOut
from core.database import get_async_db as get_async_session
from typing import List

router = APIRouter(
    prefix="/adress_samovivoz",
    tags=["Адреса самовывоза"]
)

@router.post("/", response_model=AdressOut)
async def add_adress(adress: AdressIn, session: AsyncSession = Depends(get_async_session)):
    db_adress = AdressSamovivoz(adress=adress.adress)
    session.add(db_adress)
    await session.commit()
    await session.refresh(db_adress)
    return db_adress

@router.delete("/{adress_id}")
async def delete_adress(adress_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = delete(AdressSamovivoz).where(AdressSamovivoz.id == adress_id)
    result = await session.execute(stmt)
    await session.commit()
    return {"status": "deleted"}

@router.get("/", response_model=List[AdressOut])
async def get_all(session: AsyncSession = Depends(get_async_session)):
    default_addresses = [
        "г. Москва, ул. Ленина, 10",
        "г. Санкт-Петербург, пр. Невский, 25",
        "г. Екатеринбург, ул. Мира, 5",
        "г. Казань, ул. Баумана, 12",
        "г. Новосибирск, пр. Красный, 42",
        "г. Киев, ул. Крещатик, 15",
        "г. Минск, пр. Независимости, 32",
        "г. Алматы, ул. Абая, 56",
        "г. Тбилиси, пр. Руставели, 14",
        "г. Берлин, Unter den Linden, 77",
        "г. Париж, Rue de Rivoli, 23",
        "г. Токио, район Сибуя, 1-2-3",
        "г. Нью-Йорк, Broadway, 100",
        "г. Сидней, George Street, 42",
        "г. Затупеево, ул. Пупкина, 13"
    ]
    for addr in default_addresses:
        exists_query = await session.execute(select(AdressSamovivoz).where(AdressSamovivoz.adress == addr))
        if not exists_query.scalar():
            session.add(AdressSamovivoz(adress=addr))
    await session.commit()
    result = await session.execute(select(AdressSamovivoz))
    return result.scalars().all()

@router.post("/fill_default")
async def fill_default_addresses(session: AsyncSession = Depends(get_async_session)):
    default_addresses = [
        "г. Москва, ул. Ленина, 10",
        "г. Санкт-Петербург, пр. Невский, 25",
        "г. Екатеринбург, ул. Мира, 5",
        "г. Казань, ул. Баумана, 12",
        "г. Новосибирск, пр. Красный, 42",
        "г. Киев, ул. Крещатик, 15",
        "г. Минск, пр. Независимости, 32",
        "г. Алматы, ул. Абая, 56",
        "г. Тбилиси, пр. Руставели, 14",
        "г. Берлин, Unter den Linden, 77",
        "г. Париж, Rue de Rivoli, 23",
        "г. Токио, район Сибуя, 1-2-3",
        "г. Нью-Йорк, Broadway, 100",
        "г. Сидней, George Street, 42",
        "г. Затупеево, ул. Пупкина, 13"
    ]
    for addr in default_addresses:
        exists_query = await session.execute(select(AdressSamovivoz).where(AdressSamovivoz.adress == addr))
        if not exists_query.scalar():
            session.add(AdressSamovivoz(adress=addr))
    await session.commit()
    return {"status": "filled", "count": len(default_addresses)}
