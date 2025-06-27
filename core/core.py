import asyncio
import sys
from sqlalchemy import text

from core.database import Base, async_engine, engine, session_fabrik
from core.models import (Action, Categories, Entity, Gfields, Product, Profile,
                         Reviews)
from core.add_bd_cat import listcat


if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def get_data():
    async with async_engine.connect() as conn:
        ress = await conn.execute(text("SELECT VERSION()"))
        version = ress.scalar()
        print(f"PostgreSQL Version: {version}")


# asyncio.run(get_data())
from sqlalchemy import text
from core.database import engine

def drop_all_tables_force():
    with engine.connect() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE;"))
        conn.execute(text("CREATE SCHEMA public;"))
        conn.commit()
        print("✅ Все таблицы удалены каскадно.")

def create_tables():
    Base.metadata.reflect(engine)
    drop_all_tables_force()
    Base.metadata.create_all(engine)



def insert_data():

    db_profile = Profile(
        mail="gena335@gmail.coms",
        phone="+375252185522",
        name="Генадий",
        password="37891",
    )

    db_categories = Categories(
        name_categories="электротехника", url="electrical engineering"
    )
    db_categories1 = Categories(name_categories="мебель", url="furniture")
    # db_categories = Categories(name_categories="телефоны",
    #                            url="telephons",
    #                            id_parent=1,
    #                            )
    # db_categories = Categories(name_categories="телевизоры",
    #                            url="TV",
    #                            id_parent=1,
    #                            )

    db_action = Action(action="нет акции", discount=0)
    db_action1 = Action(action="распродажа", discount=20)

    db_reviews = Reviews(
        profile_id=1,
        product_id=1,
        reviews="плохой товар!!(((",
    )
    db_reviews1 = Reviews(
        profile_id=1,
        product_id=2,
        reviews="чайник??",
    )
    db_reviews2 = Reviews(
        profile_id=1,
        product_id=2,
        reviews="ладно ок",
    )

    db_product = Product(
        name_product="чайник",
        action_id=1,
        categories_id=1,  # "электротехника"
        brand="Bosh",
        price=100,
        rating=10,
        status="статус",
        img="https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcS2Q0pNt-TXHzKJLkr3nTMFsX8LPpC7UIX9SCUDT4JJcSgp3kVuWyW36nvJUwmlq7fDB9HATY0ewXIewsn_oWTva6enJSF7Goa-wyS468AlauEfrpxFN-4Q4NmnYrn-Pw&usqp=CAc",
    )
    db_product1 = Product(
        name_product="телевизор",
        action_id=1,
        categories_id=1,
        brand="Sony",
        price=2499,
        rating=100,
        status="статус",
        img="https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcRT03OcqQBmznYxDX4YmpJtD4hZL9mDi9oQdS0KCLR4iGQyJ90uaOydTfRNtdLPRzI5sSUghZ7sPuKuHtd6szkVZjpKdrnQn5gCKUUtTKg2suXoOpEJ2kKSHLsBaYbCFfAatd30wJY&usqp=CAc",
    )
    db_product2 = Product(
        name_product="диван",
        action_id=2,
        categories_id=2,
        brand="Амимебель",
        price=2799,
        status="статус",
        img="https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcRbm8eZaYugrvnCJ473vlxXfZcqim_TvlnGxw_h93dSNUbUldrc5EVbSc3Nv3Tt7v-FyoN5z02SAy8p_VZBGi7WSiT3eeZSreXWuAXVaGUTZbhB07tw_PARd1kkQCW3-MZ7FN4ZnhV6jxk&usqp=CAc",
    )
    db_entity = Entity(
        product_id=1,
        gfields_id=1,
        name_har="size",
        cost_har=25,
    )
    db_gfields = Gfields(
        name_gfields="size",
    )

    
    with session_fabrik() as session:
        session.add_all(
            [
                db_profile,
                #db_categories,
                #db_categories1,
                db_action,
                db_action1,
            ]
        )
        

        session.commit()

        for cat in listcat:
            cat_add = Categories(**cat)
            
            session.add(cat_add)

        session.commit()


        session.add_all(
            [
                db_product,
                db_product1,
                db_product2,
            ]
        )
        session.commit() 
        session.add_all(
            [
                #db_gfields,
                db_reviews,
                db_reviews1,
                db_reviews2,
            ]
        )
        session.commit()

        session.add_all(
            [
                #db_entity,
            ]
        )
        session.commit() 


create_tables()

#insert_data()
#inset_data_andr()


insert_data()

#inset_data_andr()


