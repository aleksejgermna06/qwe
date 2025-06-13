import asyncio
import sys
from sqlalchemy import text
from core.my_insert_data import insert_data
from core.database import Base, async_engine, engine

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def get_data():
    async with async_engine.connect() as conn:
        ress = await conn.execute(text("SELECT VERSION()"))
        version = ress.scalar()
        print(f"PostgreSQL Version: {version}")


# asyncio.run(get_data())


def create_tables():
    Base.metadata.reflect(engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


create_tables()
insert_data()
