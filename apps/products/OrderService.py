from sqlalchemy import delete, select, insert
from sqlalchemy.orm import selectinload

from core.models import UserBasket, Order, OrderProcessor, Product, OrderGroup
from .models import CheckoutOrderRequest
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from typing import Optional
from core.database import get_async_db
import logging
import traceback
from sqlalchemy.orm import selectinload
from .schema import ProductInOrder, UserOrderResponse

session_fabrik = get_async_db

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
import logging

class OrderService:

    @staticmethod
    async def create_order_with_processor(order_data: CheckoutOrderRequest, id_profile: int, db: AsyncSession):
        try:
            # Получаем корзину пользователя
            result = await db.execute(select(UserBasket).where(UserBasket.id_profile == id_profile))
            basket_items = result.scalars().all()

            if not basket_items:
                raise HTTPException(status_code=404, detail="Корзина пуста")

            total_price = 0
            total_count = 0

            # Создаем OrderGroup с id_profile
            order_group = OrderGroup(id_profile=id_profile)
            db.add(order_group)
            await db.flush()  # Чтобы получить id_order_group

            for item in basket_items:
                product_result = await db.execute(select(Product).where(Product.id_product == item.id_product))
                product = product_result.scalar_one()

                total_price += product.price * item.count
                total_count += item.count

                order = Order(
                    id_product=item.id_product,
                    id_profile=id_profile,
                    id_order_group=order_group.id_order_group,  # Внимание: id_order_group
                    count=item.count
                )
                db.add(order)

            # Создаем OrderProcessor
            order_proc = OrderProcessor(
                id_order_group=order_group.id_order_group,  # Внимание: id_order_group
                price=total_price,
                count=total_count,
                status="создан",
                comment=order_data.comment,
                shipping_cost=order_data.shipping_cost,
                adress=order_data.adress
            )
            db.add(order_proc)

            # Очищаем корзину
            await db.execute(delete(UserBasket).where(UserBasket.id_profile == id_profile))
            await db.commit()

            return order_proc.id_order_proc

        except Exception as e:
            logging.error(e, exc_info=True)
            await db.rollback()
            logging.error(traceback.format_exc())
            raise HTTPException(status_code=500, detail=f"Ошибка при оформлении заказа: {str(e)}")
            #raise HTTPException(status_code=500, detail="Ошибка при оформлении заказа")

    @staticmethod
    async def get_orders_by_user(id_profile: int, db: AsyncSession):
        try:
            # Получаем все группы заказов пользователя
            result = await db.execute(select(OrderGroup).where(OrderGroup.id_profile == id_profile))
            groups = result.scalars().all()
            if not groups:
                return []

            all_orders = []
            for group in groups:
                # Заказы + продукты в группе
                order_result = await db.execute(
                    select(Order, Product)
                    .join(Product, Order.id_product == Product.id_product)
                    .where(Order.id_order_group == group.id_order_group)
                )
                orders = [
                    {
                        "order_id": order.id_order,
                        "product_id": order.id_product,
                        "product_name": product.name_product,
                        "price": product.price,
                        "count": order.count
                    }
                    for order, product in order_result.all()
                ]

                # Процессор заказа по группе
                proc_result = await db.execute(
                    select(OrderProcessor).where(OrderProcessor.id_order_group == group.id_order_group)
                )
                processor = proc_result.scalar_one_or_none()

                all_orders.append({
                    "group_id": group.id_order_group,
                    "date_created": group.date_created,
                    "orders": orders,
                    "processor": {
                        "status": processor.status if processor else None,
                        "total_price": processor.price if processor else None,
                        "shipping_cost": processor.shipping_cost if processor else None,
                        "comment": processor.comment if processor else None,
                        "adress": processor.adress if processor else None,
                    }
                })

            return all_orders

        except Exception as e:
            logging.error(e, exc_info=True)
            raise HTTPException(status_code=500, detail="Ошибка при получении заказов")
