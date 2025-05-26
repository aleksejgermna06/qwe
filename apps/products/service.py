import asyncio
import logging
import sys
from collections import defaultdict
from sqlite3 import IntegrityError

from apps.products.models import NewProduct

# Настройка политики цикла событий для Windows (нужно для asyncio)
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi import HTTPException
from sqlalchemy import delete, func, join, select

from core.database import get_async_db
from core.models import Action, Categories, Product, Reviews, metadata_obj

session_fabrik = get_async_db


class ProductService:
    @staticmethod
    async def add_product(new_Product: NewProduct):
        try:
            async for session in session_fabrik():
                db_product = Product(
                    name_product=new_Product.name_product,
                    action_id=new_Product.action_id,
                    categories_id=new_Product.categories_id,
                    brand=new_Product.brand,
                    price=new_Product.price,
                    status=new_Product.status,
                    img=new_Product.img,
                )
                session.add(db_product)
                await session.flush()
                await session.commit()
                
                return db_product.id_product
                
        except Exception as e:
            logging.error(f"adding product: {str(e)}")
            raise HTTPException(
                    status_code=500, detail=f"Ошибка при добавлении продукта: {str(e)}"
                )

    @staticmethod
    async def select_all_product(sort: int):
        try:
            async for session in session_fabrik():
                query = (
                    select(
                        Product,
                        Categories.id_categories,
                        Categories.name_categories,
                        Action.discount,
                        func.count(Reviews.id_reviews).label("number_of_reviews"),
                        Categories.id_parent,
                    )
                    .select_from(
                        join(
                            join(
                                Product,
                                Categories,
                                Product.categories_id == Categories.id_categories,
                            ),
                            Action,
                            Product.action_id == Action.id_action,
                        ).outerjoin(Reviews, Product.id_product == Reviews.product_id)
                    )
                    .group_by(
                        Product,
                        Categories.id_categories,
                        Categories.name_categories,
                        Action.discount,
                    )
                    # .order_by(func.count(reviews.id_reviews).desc())
                )
                if sort == 0:
                    query = query.order_by(Categories.id_parent.asc())
                elif sort == 1:
                    query = query.order_by(Categories.name_categories.asc())
                elif sort == 2:
                    query = query.order_by(Product.brand.asc())
                elif sort == 3:
                    query = query.order_by(Categories.id_categories.asc())
                result = await session.execute(query)
                rows = result.all()

                if not rows:
                    logging.warning(f"not found products")
                    raise HTTPException(
                        status_code=404, detail=f"Продукты не найдены"
                        
                    )
                # first_row = result.first()
                # print(f"Количество полей в результате: {len(first_row._fields)}")
                return [
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
                        "number_of_reviews": number_of_reviews,
                        "status": prod.status,
                        "img": prod.img,
                        "category": {
                            "id_categories": id_categories,
                            "name_categories": name_categories,
                        },
                    }
                    for prod, id_categories, name_categories, discount, number_of_reviews, id_parent in rows
                ]
        except Exception as e:
            logging.error(f"select products: {str(e)}")
            raise HTTPException(
                    status_code=500, detail=f"Ошибка при выводе продукта: {str(e)}"
                )
            

    @staticmethod
    async def one_product(product_id: int):
        try:
            async for session in session_fabrik():

                query = (
                    select(
                        Product,
                        Categories.id_categories,
                        Categories.name_categories,
                        Action.discount,
                        func.count(Reviews.id_reviews).label("number_of_reviews"),
                    )
                    .where(Product.id_product == product_id)
                    .select_from(
                        join(
                            join(
                                Product,
                                Categories,
                                Product.categories_id == Categories.id_categories,
                            ),
                            Action,
                            Product.action_id == Action.id_action,
                        ).outerjoin(Reviews, Product.id_product == Reviews.product_id)
                    )
                    .group_by(
                        Product,
                        Categories.id_categories,
                        Categories.name_categories,
                        Action.discount,
                    )
                )
                # query = select(product.name_product, product.price)
                result = await session.execute(query)
                db_product = result.first()
                if not db_product:
                    logging.warning(f"not found product ID {product_id}")
                    raise HTTPException(
                        status_code=404, detail=f"Продукт с ID {product_id} не найден"
                        
                    )

                prod, id_categories, name_categories, discount, number_of_reviews = (
                    db_product
                )
                res = {
                    "id_product": prod.id_product,
                    "name_product": prod.name_product,
                    "brand": prod.brand,
                    "price": prod.price,
                    "discount": discount,
                    "quantity_in_stock": prod.quantity_in_stock,
                    "rating": prod.rating,
                    "date_create": prod.date_created,
                    "date_update": prod.date_update,
                    "number_of_reviews": number_of_reviews,
                    "status": prod.status,
                    "img": prod.img,
                    "category": {
                        "id_categories": id_categories,
                        "name_categories": name_categories,
                    },
                }

                return res
        except Exception as e:
            logging.error(f"select one product: {str(e)}")
            raise HTTPException(
                    status_code=500, detail=f"Ошибка при выводе одного продукта: {str(e)}"
                )
            

    @staticmethod
    async def del_product(product_id: int):

        async for session in session_fabrik():

            try:

                check_query = select(Product).where(Product.id_product == product_id)
                result = await session.execute(check_query)
                db_product = result.scalar_one_or_none()

                if not db_product:
                    raise HTTPException(
                        status_code=404, detail=f"Продукт с ID {product_id} не найден"
                    )

                await session.delete(db_product)
                await session.commit()

                return {
                    "status": "success",
                    "message": f"Продукт {product_id} удален",
                    "deleted_product": {
                        "id": db_product.id_product,
                        "name": db_product.name_product,
                    },
                }

            except HTTPException:
                raise

            except Exception as e:
                logging.error(f"del product: {str(e)}")
                await session.rollback()
                raise HTTPException(
                    status_code=500, detail=f"Ошибка при удалении: {str(e)}"
                )
