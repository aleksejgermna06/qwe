import asyncio
import json
import sys

from sqlalchemy import text

from core.database import Base, async_engine, engine, session_fabrik
from core.models import (Action, Categories, Product, Profile, Reviews, Entity, Gfields,
                         metadata_obj)

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


def insert_data():

    db_profile = Profile(
        mail="gena335@gmail.coms",
        phone="+375252185522",
        name="Генадий",
        password="335335",
    )

    # Получение категорий

    with open("categories.json", "r", encoding="utf-8") as file:
        categories_data = json.load(file)
    categories_list = []
    for category in categories_data:
        new_category = Categories(
            name_categories=category["name_categories"],
            url=category["url"],
            id_parent=category["id_parent"]
        )
        categories_list.append(new_category)



    with session_fabrik() as session:

        session.add(db_profile)
        session.commit()


create_tables()
insert_data()
