import asyncio
import logging
import sys

from fastapi import FastAPI

from apps.categories import router as categories_roters
from apps.products import router as products_router
from core.core import create_tables, insert_data

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
app = FastAPI()
app.include_router(categories_roters)
app.include_router(products_router)

create_tables()
insert_data()
