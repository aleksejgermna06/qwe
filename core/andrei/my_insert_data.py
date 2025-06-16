import json
from core.database import session_fabrik
from core.models import (Action, Categories, Product, Profile, Entity, Gfields)


def insert_data():

    db_profile = Profile(
        mail="gena335@gmail.coms",
        phone="+375252185522",
        name="Генадий",
        password="335335",
    )

    # Получение категорий

    with open("core/andrei/categories.json", "r", encoding="utf-8") as file:
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

    with open("core/andrei/actions.json", "r", encoding="utf-8") as file:
        actions_data = json.load(file)
    actions_list = []
    for action in actions_data:
        new_action = Action(
            action=action["action"],
            discount=action["discount"]
        )
        actions_list.append(new_action)

    # Получение продуктов

    with open("core/andrei/product.json", "r", encoding="utf-8") as file:
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

    with open("core/andrei/gfields.json", "r", encoding="utf-8") as file:
        gfields_data = json.load(file)
    gfields_list = []
    for gfield in gfields_data:
        new_gfield = Gfields(
            name_gfields=gfield["name_gfields"]
        )
        gfields_list.append(new_gfield)

    # Получение значений характеристик

    with open("core/andrei/entity.json", "r", encoding="utf-8") as file:
        entities_data = json.load(file)
    entities_list = []
    for entity in entities_data:
        new_entity = Entity(
            product_id=entity["id_product"],
            gfields_id=entity["id_gfields"],
            name_har=entity["name_har"],
            cost_har=entity["cost_har"]
        )
        entities_list.append(new_entity)

    with session_fabrik() as session:

        session.add(db_profile)
        session.flush()

        session.add_all(categories_list)
        session.flush()

        session.add_all(actions_list)
        session.flush()

        session.add_all(products_list)
        session.flush()

        session.add_all(gfields_list)
        session.flush()

        session.add_all(entities_list)
        print(f"Начинаем вставку {len(entities_list)} записей в Entity")
        session.flush()
        session.commit()
