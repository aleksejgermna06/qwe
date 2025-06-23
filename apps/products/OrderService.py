from sqlalchemy import delete, select, insert
from core.models import UserBasket, Order, OrderProcessor, Product
from .models import CheckoutOrderRequest
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from typing import Optional
from core.database import get_async_db
import logging
import traceback

session_fabrik = get_async_db

class OrderService:

    @staticmethod
    async def create_order_with_processor_by_ids(
            basket_item_ids: list[int],
            profile_id: int,
            comment: Optional[str] = None,
            shipping_cost: Optional[int] = 0,
            adress: Optional[str] = None,
            organization: Optional[str] = None
    ):
        try:
            async for session in session_fabrik():
                # Получаем только нужные элементы из корзины пользователя
                result = await session.execute(
                    select(UserBasket).where(
                        UserBasket.id_us_storage.in_(basket_item_ids),
                        UserBasket.id_profile == profile_id
                    )
                )
                basket_items = result.scalars().all()

                if not basket_items:
                    raise HTTPException(status_code=404, detail="Переданные товары не найдены в корзине")

                total_price = 0
                order_ids = []

                for item in basket_items:
                    product_result = await session.execute(
                        select(Product).where(Product.id_product == item.id_product)
                    )
                    product = product_result.scalar_one_or_none()

                    if not product:
                        continue  # Пропускаем, если товара нет

                    count = item.count or 1
                    total_price += product.price * count

                    new_order = Order(
                        id_product=product.id_product,
                        id_profile=profile_id,
                        count=count
                    )
                    session.add(new_order)
                    await session.flush()
                    order_ids.append(new_order.id_order)

                if not order_ids:
                    raise HTTPException(status_code=400, detail="Не удалось создать ни одного заказа")

                order_proc = OrderProcessor(
                    id_order=order_ids[0],
                    price=total_price,
                    count=sum([item.count or 1 for item in basket_items]),
                    status="создан",
                    comment=comment,
                    shipping_cost=shipping_cost,
                    adress=adress,
                    organization=organization
                )
                session.add(order_proc)

                # Удаляем оформленные позиции из корзины
                await session.execute(
                    delete(UserBasket).where(
                        UserBasket.id_us_storage.in_(basket_item_ids),
                        UserBasket.id_profile == profile_id
                    )
                )

                await session.commit()
                return order_proc.id_order_proc

        except Exception as e:
            logging.error(f"Order creation error: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=f"Ошибка при оформлении заказа: {str(e)}")



