import asyncio
import logging
import sys
import traceback
from collections import defaultdict

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


from fastapi import HTTPException
from sqlalchemy import outerjoin,join,func, select

from core.database import get_async_db
from core.models import Action, Categories, Product, ComparisonStore

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
                    outerjoin(
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
                    raise HTTPException(status_code=404, detail=f"Категории не найдены")

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
                            "url": category.url,
                            # "products": [
                            #     {
                            #         "id_product": p.id_product,
                            #         "name_product": p.name_product,
                            #         "price": p.price,
                            #     }
                            #     for p in products
                            # ],
                        }
                    )

            return response
        except Exception as e:
            logging.error(f"select all categor: {traceback.format_exc()}")
            raise HTTPException(
                status_code=500, detail=f"Ошибка при выводе категории: {str(e)}"
            )

    @staticmethod
    async def select_one_cat(url: str):
        try:
            async for session in session_fabrik():
                query = (
                    select(Categories, Product, Action.discount)
                    
                    .select_from(
                        outerjoin(
                            Categories,
                            Product,
                            Categories.id_categories == Product.categories_id,
                        )
                        .join(
                            Action,
                            Product.action_id == Action.id_action,
                        )
                    )
                    .where(Categories.url == url)
                   
                )

                result = await session.execute(query)
                rows = result.all()

                if not rows:
                    logging.warning(f"not found cat {url}")
                    raise HTTPException(
                        status_code=404, detail=f"Категория не найдена {url}"
                    )

                categories_dict = defaultdict(list)
                for cat, prod, discount in rows:
                    categories_dict[cat].append((prod,discount))

                response = []
                
                for category, products in categories_dict.items():
                    category_data = {
                        "id_categories": category.id_categories,
                        "name_categories": category.name_categories,
                        "id_parent": category.id_parent,
                        "url": category.url,
                        "products": []
                    }
                    
                    # Добавляем продукты только если они есть
                    if products is not None:
                        category_data["products"] = [
                            {
                                
                                "id_product": p.id_product,
                                "name_product": p.name_product,
                                "brand": p.brand,
                                "price": p.price,
                                "discount": discount ,
                                "quantity_in_stock": p.quantity_in_stock,
                                "rating": p.rating,
                                "date_create": p.date_created,
                                "date_update": p.date_update,
                                "status": p.status,
                                "img": p.img,
                            }
                            for p,discount  in products
                            if p is not None
                        ]
                    
                    response.append(category_data)

            return response[0]
        except Exception as e:
            logging.error(f"select one categor: {traceback.format_exc()}")
            raise HTTPException(
                status_code=500, detail=f"Ошибка при выводе одной категории: {str(e)}"
            )
        
    @staticmethod
    async def select_cat_comparison(id_profile: int):
        try:
            async for session in session_fabrik():
                query = (
                    select(

                        Categories,
                        func.count(Product.id_product).label("count_prod")
                    )
                    .select_from(
                        
                        outerjoin(ComparisonStore, Product, ComparisonStore.product_id == Product.id_product)
                        .join(Categories, Product.categories_id == Categories.id_categories)
                    )
                    .where(ComparisonStore.profile_id == id_profile)
                    .group_by(Categories.name_categories, Categories.id_categories)
                   
                )

                result = await session.execute(query)
                rows = result.all()
                
                if not rows:
                    logging.warning(f"not found cat {id_profile}")
                    raise HTTPException(
                        status_code=404, detail=f"Категория не найдена {id_profile}"
                    )

            return [
                {
                    "category": cat.name_categories,
                    "count": count,

                }
                for  cat, count in rows
            ]
        except Exception as e:
            logging.error(f"select one categor: {traceback.format_exc()}")
            raise HTTPException(
                status_code=500, detail=f"Ошибка при выводе одной категории: {str(e)}"
            )