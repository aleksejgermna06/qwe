import asyncio
import logging
import sys
import traceback
from collections import defaultdict

from apps.categories.schema import CatProdOut

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


from fastapi import HTTPException
from sqlalchemy import outerjoin,join,func, select, case, exists, and_

from core.database import get_async_db
from core.models import Action, Categories, Product, ComparisonStore, UserBasket#, UserAction
from apps.user_actions.models import UserAction

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
    async def select_one_cat(url: str, id_profile: int):
        try:
            async for session in session_fabrik():
                query = (
                    select(Categories, 
                           Product,
                            Action.discount,
                            case(
                            (
                                exists().where(
                                    and_(
                                        UserBasket.id_product == Product.id_product,
                                        UserBasket.id_profile == id_profile
                                    )
                                ), 
                                True
                            ),
                            else_=False
                        ).label("in_cart"),
                        case(
                            (
                                exists().where(
                                    and_(
                                        UserAction.product_id == Product.id_product,
                                        UserAction.profile_id == id_profile
                                    )
                                ),
                                True
                            ),
                            else_=False
                        ).label("in_fav")
                        
                        )
                    
                    .select_from(
                        outerjoin(
                            Categories,
                            Product,
                            Categories.id_categories == Product.categories_id,
                        )
                        .outerjoin(
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
                for cat, prod, discount, in_cart, in_fav in rows:
                    categories_dict[cat].append((prod,discount, in_cart,in_fav))

                response = []

                for category, products in categories_dict.items():
                    category_data = {
                        "id_categories": category.id_categories,
                        "name_categories": category.name_categories,
                        "id_parent": category.id_parent,
                        "url": category.url,
                        "products": []
                    }

                    if products is not None:
                        category_data["products"] = [
                            {
                                "id_product": p.id_product,
                                "name_product": p.name_product,
                                "brand": p.brand,
                                "price": p.price,
                                "discount": discount,
                                "quantity_in_stock": p.quantity_in_stock,
                                "rating": p.rating,
                                "date_create": p.date_created,
                                "date_update": p.date_update,
                                "status": p.status,
                                "img": p.img,
                                "in_cart": in_cart,
                                "in_fav": in_fav,
                            }
                            for p,discount,in_cart, in_fav  in products
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
                        ComparisonStore
                    )
                    .outerjoin(Product, ComparisonStore.product_id == Product.id_product)
                    .join(Categories, Product.categories_id == Categories.id_categories)
                    .where(ComparisonStore.profile_id == id_profile)
                    .group_by(Categories.name_categories,Categories.id_categories)
                   
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
                    "url": cat.url,
                    "count": count,

                }
                for  cat, count in rows
            ]
        except Exception as e:
            logging.error(f"select one categor: {traceback.format_exc()}")
            raise HTTPException(
                status_code=500, detail=f"Ошибка при выводе одной категории: {str(e)}"
            )
        
    @staticmethod
    async def add_product_comsommer(id_profile: int,product_id: int):
        try:
            async for session in session_fabrik():
                db_product = ComparisonStore(
                    profile_id = id_profile,
                    product_id = product_id,
                )
                session.add(db_product)
                await session.flush()
                await session.commit()

                return db_product.product_id

        except Exception as e:
            logging.error(f"adding product from compaire: {traceback.format_exc()}")

            raise HTTPException(
                status_code=500, detail=f"Ошибка при добавлении продукта в сравнение: {str(e)}"
            )

    @staticmethod
    async def select_cat_prod_comparison(id_profile: int, url: int):
        try:
            async for session in session_fabrik():
                query1=select(Categories.id_categories).where(Categories.url==url)
                data_id = await session.execute(query1)
                id_cat = data_id.scalar_one_or_none()
                if not id_cat:
                    raise HTTPException(status_code=404, detail="Category not found")
                
                query = (
                   select(Product,
                          Action.action,
                          case(
                            (
                                exists().where(
                                    and_(
                                        UserBasket.id_product == Product.id_product,
                                        UserBasket.id_profile == id_profile
                                    )
                                ), 
                                True
                            ),
                            else_=False
                        ).label("in_cart"),
                         case(
                            (
                                exists().where(
                                    and_(
                                        UserAction.product_id == Product.id_product,
                                        UserAction.profile_id == id_profile
                                    )
                                ),
                                True
                            ),
                            else_=False
                        ).label("in_fav")
                        )
                    .join(ComparisonStore, ComparisonStore.product_id == Product.id_product)
                    .join(Action, Product.action_id==Action.id_action)
                    .where(
                        ComparisonStore.profile_id == id_profile,
                        Product.categories_id == id_cat
                    )
                )

                result = await session.execute(query)
                rows = result.all()
                
                if not rows:
                    logging.warning(f"not found cat {id_profile}")
                    raise HTTPException(
                        status_code=404, detail=f"Категория не найдена {id_profile}"
                    )

            return [
                # CatProdOut(
                #         id_product = prod.id_product,
                #         name_product=prod.name_product,
                #         brand = prod.brand,
                #         price = prod.price,
                #         discount = discount,
                #         quantity_in_stock = prod.quantity_in_stock,
                #         rating = prod.rating,
                #         date_create = prod.date_created,
                #         date_update = prod.date_update,
                #         #"number_of_reviews": number_of_reviews,
                #         status = prod.status,
                #         img = prod.img,
                #         in_cart =in_cart,
                # )
                {
                    "id_product": prod.id_product,
                    "name_product": prod.name_product,
                    "brand": prod.brand,
                    "price": prod.price,
                    "discount": discount,
                    "quantity_in_stock": prod.quantity_in_stock,
                    "rating": prod.rating,
                    "date_create": prod.date_created,
                    "date_update": prod.date_update,
                    #"number_of_reviews": number_of_reviews,
                    "status": prod.status,
                    "img": prod.img,
                    "in_cart": in_cart,
                    "in_fav": in_fav,

                }
                for  prod,discount, in_cart, in_fav in rows
            ]
        except Exception as e:
            logging.error(f"select one categor: {traceback.format_exc()}")
            raise HTTPException(
                status_code=500, detail=f"Ошибка при выводе одной категории: {str(e)}"
            )

    @staticmethod
    async def del_product_comp(product_id: int, profile_id: int):

        async for session in session_fabrik():

            try:

                check_query = select(ComparisonStore).where(ComparisonStore.product_id == product_id,ComparisonStore.profile_id ==profile_id )
                result = await session.execute(check_query)
                db_product = result.scalar_one_or_none()
                
                if not db_product:
                    raise HTTPException(
                        status_code=404, detail=f"Продукт с ID {product_id} не найден"
                    )

                await session.delete(db_product)
                await session.commit()

                return {
                    product_id
                    
                }

            except HTTPException:
                raise

            except Exception as e:
                logging.error(f"del product: {traceback.format_exc()}")
                await session.rollback()
                raise HTTPException(
                    status_code=500, detail=f"Ошибка при удалении: {str(e)}"
                )
            
    @staticmethod
    async def del_cat_comp(url: str, profile_id: int):

        async for session in session_fabrik():

            try:
                query1=select(Categories.id_categories).where(Categories.url==url)
                data_id = await session.execute(query1)
                id_cat = data_id.scalar_one_or_none()
                if not id_cat:
                    raise HTTPException(status_code=404, detail="Category not found")
                
                check_query = (
                                select(ComparisonStore)
                                .join(Product, Product.id_product==ComparisonStore.product_id)

                                .where( Product.categories_id==id_cat, ComparisonStore.profile_id==profile_id)
                                
                                
                            )
                result = await session.execute(check_query)
                db_product = result.scalars().all()

                
                for product in db_product:
                    await session.delete(product)
                
                await session.commit()

                return url
                    
                

            except HTTPException:
                raise

            except Exception as e:
                logging.error(f"del product: {traceback.format_exc()}")
                await session.rollback()
                raise HTTPException(
                    status_code=500, detail=f"Ошибка при удалении: {str(e)}"
                )
