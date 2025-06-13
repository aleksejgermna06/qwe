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

    # Получение акций

    with open("actions.json", "r", encoding="utf-8") as file:
        actions_data = json.load(file)
    actions_list = []
    for action in actions_data:
        new_action = Action(
            action=action["action"],
            discount=action["discount"]
        )
        actions_list.append(new_action)

    # Получение продуктов

    with open("product.json", "r", encoding="utf-8") as file:
        products_data = json.load(file)
    products_list = []
    for product in products_data:
        new_product = Product(
            action_id=product["action_id"],
            categories_id=product["categories_id"],
            date_created=product["date_created"],
            date_update=product["date_update"],
            name_product=product["name_product"],
            brand=product["brand"],
            price=product["price"],
            quantity_in_stock=product["quantity_in_stock"],
            rating=product["rating"],
            status=product["status"],
            img=product["img"]
        )
        products_list.append(new_product)

    # Получение характеристик

    with open("gfields.json", "r", encoding="utf-8") as file:
        gfields_data = json.load(file)
    gfields_list = []
    for gfield in gfields_data:
        new_gfield = Gfields(
            name_gfields=gfield["name_gfields"]
        )
        gfields_list.append(new_gfield)

    # Получение значений характеристик

    with open("entity.json", "r", encoding="utf-8") as file:
        entities_data = json.load(file)
    entities_list = []
    for entity in entities_data:
        new_entity = Entity(
            product_id=entity["id_product"],
            gfields_id=entity["id_gfields"],
            cost_har=entity["cost_har"]
        )
        entities_list.append(new_entity)

    with session_fabrik() as session:

        session.add(db_profile)
        session.commit()

        session.add_all(categories_list)
        session.commit()

        session.add_all(actions_list)
        session.commit()

        session.add_all(products_list)
        session.commit()

        session.add_all(gfields_list)
        session.commit()

        session.add_all(entities_list)
        session.commit()


create_tables()
insert_data()
