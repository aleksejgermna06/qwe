import asyncio
import logging
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apps.categories import router as categories_roters
from apps.products import router_brand, router_basket,router as products_router
from core.core import create_tables, insert_data

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
origins = [
    "http://178.121.56.9:5432"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(categories_roters)
app.include_router(products_router)
app.include_router(router_basket)
app.include_router(router_brand)

create_tables()
insert_data()
