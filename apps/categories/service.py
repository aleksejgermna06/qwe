import asyncio
import logging
import sys
from collections import defaultdict
import traceback

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi import HTTPException
from sqlalchemy import join, select

from core.database import get_async_db
from core.models import Action, Categories, Product

session_fabrik = get_async_db


async def heder():
    cate = await select_categories()
    act = await select_action()
    return {"categories": cate, "actions": act}


async def select_categories():
    async for session in session_fabrik():
        query = select(Categories)
        result = await session.execute(query)
        return result.scalars().all()


async def select_action():
    async for session in session_fabrik():
        query = select(Action.action).distinct()
        result = await session.execute(query)
        return result.scalars().all()


class CategorieService:
    @staticmethod
    async def select_all_cat(sort: int):
        try:
            async for session in session_fabrik():
                query = select(Categories, Product).select_from(
                    join(
                        Categories,
                        Product,
                        Categories.id_categories == Product.categories_id,
                    )
                )
                if sort == 0:
                    query = query.order_by(Categories.id_parent.asc())
                elif sort == 1:
                    query = query.order_by(Categories.name_categories.asc())

                result = await session.execute(query)
                rows = result.all()

                if not rows:
                    logging.warning(f"not found cats")
                    raise HTTPException(
                        status_code=404, detail=f"Категории не найдены"

                    )

                categories_dict = defaultdict(list)
                for cat, prod in rows:
                    categories_dict[cat].append(prod)

                response = []
                for category, products in categories_dict.items():
                    response.append(
                        {
                            "id_categories": category.id_categories,
                            "name_categories": category.name_categories,
                            "id_parent": category.id_parent,
                            "products": [
                                {
                                    "id_product": p.id_product,
                                    "name_product": p.name_product,
                                    "price": p.price,
                                }
                                for p in products
                            ],
                        }
                    )

            return response
        except Exception as e:
            logging.error(f"select all categor: {traceback.format_exc()}")
            raise HTTPException(
                status_code=500, detail=f"Ошибка при выводе категории: {str(e)}"
            )

    @staticmethod
    async def select_one_cat(id_cat: int):
        try:
            async for session in session_fabrik():
                query = (
                    select(Categories, Product)
                    .where(Categories.id_categories == id_cat)
                    .select_from(
                        join(
                            Categories,
                            Product,
                            Categories.id_categories == Product.categories_id,
                        )
                    )
                )

                result = await session.execute(query)
                rows = result.all()

                if not rows:
                    logging.warning(f"not found cat {id_cat}")
                    raise HTTPException(
                        status_code=404, detail=f"Категория не найдена {id_cat}"

                    )

                categories_dict = defaultdict(list)
                for cat, prod in rows:
                    categories_dict[cat].append(prod)

                response = []
                for category, products in categories_dict.items():
                    response.append(
                        {
                            "id_categories": category.id_categories,
                            "name_categories": category.name_categories,
                            "id_parent": category.id_parent,
                            "products": [
                                {
                                    "id_product": p.id_product,
                                    "name_product": p.name_product,
                                    "price": p.price,
                                }
                                for p in products
                            ],
                        }
                    )

            return response
        except Exception as e:
            logging.error(f"select one categor: {traceback.format_exc()}")
            raise HTTPException(
                status_code=500, detail=f"Ошибка при выводе одной категории: {str(e)}"
            )