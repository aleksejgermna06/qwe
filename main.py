# from fastapi import FastAPI
# from apps.users import router as auth_router
# from apps.categories import router as categories_roters
# from apps.products import router as products_router
# import uvicorn
#
# from core.models import Base
# from core.database import engine
# from core.core import create_tables, insert_data
#
# Base.metadata.create_all(bind=engine)
#
#
# app = FastAPI()
# app.include_router(auth_router)
# app.include_router(categories_roters)
# app.include_router(products_router)
#
#
# insert_data()
#
# if __name__ == "__main__":
#     uvicorn.run("main:app", reload=True)

import asyncio
import logging
import sys

from fastapi import FastAPI

from apps.categories import router as categories_roters
from apps.products import router_basket,router as products_router
from core.core import create_tables, insert_data
from apps.users import router as auth_router

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
app = FastAPI()
app.include_router(auth_router)
app.include_router(categories_roters)
app.include_router(products_router)
app.include_router(router_basket)

create_tables()
insert_data()
