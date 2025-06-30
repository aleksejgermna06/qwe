import asyncio
import logging
import sys

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apps.categories import router as categories_roters
from apps.products import router_brand,router_order ,router_basket,router as products_router
from core.core import create_tables, insert_data
from apps.users import router as auth_router
from apps.users.routers import router1 as user_router
from apps.user_actions.routers import router as user_actions_router

from core.andrei.my_insert_data import insert_data as inset_data_andr
from apps.adress_samovivoz import routers as adress_router


if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

logging.basicConfig(
    level=logging.INFO,
    filename="py_log.log",
    filemode="w",
    format="%(asctime)s %(levelname)s %(message)s",
)
origins = [
    "http://178.120.87.89:5173",
    "http://localhost:5173",
    "http://localhost:80",
    "http://0.0.0.0:5432",
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

app.include_router(auth_router)
app.include_router(user_actions_router)
app.include_router(user_router)
app.include_router(router_order)

app.include_router(adress_router.router)


create_tables()

inset_data_andr()


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
