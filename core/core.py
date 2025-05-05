
import asyncio
import sys
from sqlalchemy import text
from core.database import engine, async_engine, session_fabrik, Base
from models import metadata_obj

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def get_data():
    async with async_engine.connect() as conn: 
        ress = await conn.execute(text("SELECT VERSION()"))
        version = ress.scalar() 
        print(f"PostgreSQL Version: {version}")


asyncio.run(get_data()) 


def create_tables():
    
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
   
   

""" def insert_data():
    wooker_bobr=Worker(username="bobr")
    with session_fabrik() as session:
        session.add(wooker_bobr)
        session.commit() """
       

create_tables()
#insert_data()
