import asyncio
import logging
import math
import sys
import traceback
from collections import defaultdict

from apps.products.models import AddProdBask, NewProduct

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi import HTTPException

from sqlalchemy import delete, func, join, select, cast, Numeric, nulls_last, case, and_, exists,update

from core.database import get_async_db
from core.models import Action, Categories, Product, Reviews, metadata_obj, UserBasket, Entity, Gfields, Categories

session_fabrik = get_async_db


class ProductService:

    @staticmethod
    async def get_many_products(product_ids: list[int]) -> list[dict]:
        try:
            async for session in session_fabrik():
                query = (
                    select(
                        Product,
                        Categories.id_categories,
                        Categories.name_categories,
                        Action.discount,
                        func.count(Reviews.id_reviews).label("number_of_reviews"),
                        Categories.url,
                    )
                    .select_from(Product)
                    .join(Categories, Product.categories_id == Categories.id_categories)
                    .join(Action, Product.action_id == Action.id_action)
                    .outerjoin(Reviews, Product.id_product == Reviews.product_id)
                    .where(Product.id_product.in_(product_ids))
                    .group_by(
                        Product,
                        Categories.id_categories,
                        Categories.name_categories,
                        Action.discount,
                        Categories.url,
                    )
                )

                result = await session.execute(query)
                rows = result.all()

                products = []
                for row in rows:
                    prod = row[0]
                    products.append({
                        "id_product": prod.id_product,
                        "name_product": prod.name_product,
                        "brand": prod.brand,
                        "price": prod.price,
                        "discount": row[3],
                        "quantity_in_stock": prod.quantity_in_stock,
                        "rating": prod.rating,
                        "number_of_reviews": row[4],
                        "status": prod.status,
                        "img": prod.img,
                    })

                return products

        except Exception:
            logging.error(f"Error getting many products: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail="Ошибка при получении списка товаров")

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
            logging.error(f"adding product: {traceback.format_exc()}")

            raise HTTPException(
                status_code=500, detail=f"Ошибка при добавлении продукта: {str(e)}"
            )

    @staticmethod
    async def select_all_product(sort: int, id_profile: int):

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
                        Categories.url,
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
                        "in_cart": in_cart,
                        "category": {
                            "id_categories": id_categories,
                            "name_categories": name_categories,
                            "url": url,
                        },
                    }

                    for prod, id_categories, name_categories, discount, number_of_reviews, id_parent, url, in_cart in
                    rows

                ]
        except Exception as e:
            logging.error(f"select products: {traceback.format_exc()}")
            raise HTTPException(
                status_code=500, detail=f"Ошибка при выводе продукта: {str(e)}"
            )

    @staticmethod
    async def filter_product(
            brand: str,
            price_filtr: str,
            popular: int,
            min_price: int,
            max_price: int,
            page: int,
            size: int,
            id_profile: int

    ):
        try:
            async for session in session_fabrik():
                offset_min = page * size
                offset_max = (page + 1) * size
                query = (
                    select(
                        Product,
                        Categories.id_categories,
                        Categories.name_categories,
                        Action.discount,
                        func.count(Reviews.id_reviews).label("number_of_reviews"),
                        Categories.id_parent,
                        Categories.url,

                        case(
                            (
                                exists().where(
                                    and_(
                                        UserBasket.id_product == Product.id_product,
                                        UserBasket.id_profile == id_profile
                                    )
                                ),
                                "true"
                            ),
                            else_="false"
                        ).label("in_cart")
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

                if brand is not None:
                    query = query.where(Product.brand == brand)

                if (
                        min_price is not None
                        and max_price is not None
                        and min_price > max_price
                ):
                    raise HTTPException(
                        status_code=400,
                        detail="Минимальная цена не может быть больше максимальной",
                    )

                if min_price is not None and max_price is not None:
                    query = query.where(
                        Product.price >= min_price, Product.price <= max_price
                    )
                elif min_price is not None:
                    query = query.where(Product.price >= min_price)
                elif max_price is not None:
                    query = query.where(Product.price <= max_price)

                if popular is not None and price_filtr is not None:
                    raise HTTPException(
                        status_code=400,
                        detail="Невозможно сортировать спазу по этим двум параметрам",
                    )

                if popular is not None:
                    query = query.order_by(Product.rating.desc())

                elif price_filtr is not None:
                    if price_filtr == "desc":
                        query = query.order_by(Product.price.desc())
                    else:
                        query = query.order_by(Product.price.asc())

                result = await session.execute(query)
                rows = result.all()
                products_data = [
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
                        "in_cart": in_cart,
                        "category": {
                            "id_categories": id_categories,
                            "name_categories": name_categories,
                            "url": url,
                        },
                    }

                    for prod, id_categories, name_categories, discount, number_of_reviews, id_parent, url, in_cart in
                    rows[

                    offset_min:offset_max
                    ]
                ]

                if not products_data:
                    logging.warning(f"not found products")
                    raise HTTPException(status_code=404, detail=f"Продукты не найдены")

                """ rowss=rows[offset_min:offset_max]+[
                    {
                        "page": page,
                        "size": size,
                        "total": math.ceil(len(rows)/size)-1,
                    }
                ] """

                # first_row = result.first()
                # print(f"Количество полей в результате: {len(first_row._fields)}")
                return {
                    "data": products_data,
                    "pagination": {
                        "page": page,
                        "size": size,
                        "total": math.ceil(len(rows) / size) - 1,
                    },
                }
        except Exception as e:
            logging.error(f"select products: {traceback.format_exc()}")
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
                        Categories.url,
                        Entity,
                        Gfields,
                    )
                    .select_from(Product)
                    .join(Categories, Product.categories_id == Categories.id_categories)
                    .join(Action, Product.action_id == Action.id_action)
                    .join(Entity, Product.id_product == Entity.product_id)
                    .join(Gfields, Gfields.id_gfields == Entity.gfields_id)
                    .outerjoin(Reviews, Product.id_product == Reviews.product_id)
                    .where(Product.id_product == product_id)
                    .group_by(
                        Product,
                        Categories.id_categories,
                        Categories.name_categories,
                        Action.discount,
                        Categories.url,
                        Entity,
                        Gfields,
                    )
                )

                result = await session.execute(query)
                rows = result.all()  # Получаем все строки

                if not rows:
                    logging.warning(f"not found product ID {product_id}")
                    raise HTTPException(
                        status_code=404, detail=f"Продукт с ID {product_id} не найден"
                    )

                first_row = rows[0]
                prod = first_row[0]

                characteristics_dict = defaultdict(list)
                for row in rows:
                    _, _, _, _, _, _, entity, gfields = row
                    characteristics_dict[gfields].append(entity)

                res = {
                    "id_product": prod.id_product,
                    "name_product": prod.name_product,
                    "brand": prod.brand,
                    "price": prod.price,
                    "discount": first_row[3],
                    "quantity_in_stock": prod.quantity_in_stock,
                    "rating": prod.rating,
                    # "date_create": prod.date_created,
                    # "date_update": prod.date_update,
                    "number_of_reviews": first_row[4],
                    "status": prod.status,
                    "img": prod.img,
                    "category": {
                        "id_categories": first_row[1],
                        "name_categories": first_row[2],
                        "url": first_row[5],
                    },
                    "characteristics": [
                        {
                            "name_characteristic": gfields.name_gfields,
                            "characteristics": [
                                {
                                    "name": entity.name_har,
                                    "count": entity.cost_har,
                                }
                                for entity in entities
                            ],
                        }
                        for gfields, entities in characteristics_dict.items()
                    ],
                }

                return res

        except Exception as e:
            logging.error(f"select one product: {traceback.format_exc()}")
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
                logging.error(f"del product: {traceback.format_exc()}")
                await session.rollback()
                raise HTTPException(
                    status_code=500, detail=f"Ошибка при удалении: {str(e)}"
                )

    @staticmethod
    async def add_product_bask(add_prod_bask: AddProdBask, profile_id: int):
        try:
            async for session in session_fabrik():
                db_bask = UserBasket(
                    id_profile=profile_id,
                    id_product=add_prod_bask.id_product,
                    
                )
                session.add(db_bask)
                await session.flush()
                await session.commit()

                return db_bask.id_us_storage

        except Exception as e:
            logging.error(f"adding product from basket: {traceback.format_exc()}")

            raise HTTPException(
                status_code=500,
                detail=f"Ошибка при добавлении продукта в корзину: {str(e)}",
            )

    @staticmethod
    async def del_product_bask(id_prod: int, profile_id):

        async for session in session_fabrik():

            try:

                check_query = select(UserBasket).where(
                    UserBasket.id_product == id_prod,
                    UserBasket.id_profile==profile_id
                )
                result = await session.execute(check_query)
                db_bask = result.scalars().all()

                if not db_bask:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Номенкулатура с ID {id_prod} не найден",
                    )

                await session.delete(db_bask)
                await session.commit()

                return {
                    "status": "success",
                    "message": f"Номенкулатура {id_prod} удалена",
                    
                }

            except HTTPException:
                raise

            except Exception as e:
                logging.error(f"del product from basket: {traceback.format_exc()}")
                await session.rollback()
                raise HTTPException(
                    status_code=500, detail=f"Ошибка при удалении из корзины: {str(e)}"
                )

    @staticmethod
    async def sellect_product_bask(id_user: int):

        try:
            async for session in session_fabrik():
                query = (
                    select(
                        UserBasket,
                        Product,
                    )
                    .select_from(
                        join(
                            join(
                                UserBasket,
                                Product,
                                Product.id_product == UserBasket.id_product,
                            ),
                            Action,
                            Product.action_id == Action.id_action,
                        )
                    )
                    .where(
                        UserBasket.id_profile == id_user,
                    )
                )

                result = await session.execute(query)
                rows = result.all()

                """ if not rows:
                    logging.warning(f"not found products")
                    raise HTTPException(
                        status_code=404, detail=f"Продукты не найдены"

                    ) """
                # first_row = result.first()
                # print(f"Количество полей в результате: {len(first_row._fields)}")
                return [
                    {
                        "id_product": prod.id_product,
                        "name_product": prod.name_product,
                        "all_price": prod.price * us_bask.count,
                        "status": prod.status,
                        "img": prod.img,
                        "count": us_bask.count,
                    }
                    for us_bask, prod in rows
                ]
        except Exception as e:
            logging.error(f"select products bask: {traceback.format_exc()}")
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка при выводе продукта из корзины: {str(e)}",
            )

    @staticmethod
    async def select_brands():
        try:
            async for session in session_fabrik():
                query = select(Product.brand).distinct()
                result = await session.execute(query)
                rows = result.scalars().all()

                return rows

        except Exception as e:
            logging.error(f"select brands: {traceback.format_exc()}")

            raise HTTPException(
                status_code=500, detail=f"Ошибка при выводе брэнда: {str(e)}"
            )

    @staticmethod
    async def serch(letters: str):
        try:
            async for session in session_fabrik():
                query = select(Product).filter(
                    func.lower(Product.name_product).startswith(func.lower(letters))
                )
                result = await session.execute(query)
                rows = result.scalars().all()
                prod = {"products": [], "categories": []}
                prod["products"] = [
                    {
                        "id_product": pr.id_product,
                        "name_product": pr.name_product,

                    }
                    for pr in rows
                ]
                query = select(Categories).filter(
                    func.lower(Categories.name_categories).startswith(func.lower(letters))
                )
                result = await session.execute(query)
                rows = result.scalars().all()
                prod["categories"] = [
                    {
                        "name_product": ct.name_categories,
                        "url": ct.url,
                    }
                    for ct in rows
                ]

                return prod

        except Exception as e:
            logging.error(f"select brands: {traceback.format_exc()}")

            raise HTTPException(
                status_code=500, detail=f"Ошибка при выводе брэнда: {str(e)}"
            )
        
    @staticmethod
    async def put_product_bask(id_prod: int, profile_id, new_count):

        async for session in session_fabrik():

            try:

                check_query = update(UserBasket).where(
                    UserBasket.id_product == id_prod,
                    UserBasket.id_profile==profile_id
                ).values(count=new_count)
                await session.execute(check_query)
                await session.commit()

               

                return id_prod

            except HTTPException:
                raise

            except Exception as e:
                logging.error(f"del product from basket: {traceback.format_exc()}")
                await session.rollback()
                raise HTTPException(
                    status_code=500, detail=f"Ошибка при изменении товара в корзине: {str(e)}"
                )

    