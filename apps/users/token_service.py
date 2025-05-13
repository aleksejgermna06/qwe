from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.models import Token

async def create_token_record(db: AsyncSession, user_id: int, tokens: dict):
    token_record = Token(
        user_id=user_id,
        access_token=tokens['access_token'],
        refresh_token=tokens['refresh_token'],
        expires_at=tokens['expires_at']
    )
    db.add(token_record)
    await db.commit()
    return token_record