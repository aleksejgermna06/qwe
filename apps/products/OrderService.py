from sqlalchemy import delete, select, insert
from core.models import UserBasket, Order, OrderProcessor, Product
from .models import CheckoutOrderRequest
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException


class OrderService:

    @staticmethod
    async def create_order_with_processor(order_data: CheckoutOrderRequest, id_profile: int, db: AsyncSession):
        basket_ids = [item.id_us_storage for item in order_data.basket_items]

        result = await db.execute(
            select(UserBasket).where(
                UserBasket.id_us_storage.in_(basket_ids),
                UserBasket.id_profile == id_profile
            )
        )
        basket_items = result.scalars().all()

        if not basket_items:
            raise HTTPException(status_code=404, detail="Корзина пуста или товары не найдены")

        total_price = 0
        order_ids = []

        for item in basket_items:

            product_result = await db.execute(
                select(Product).where(Product.id_product == item.id_product)
            )
            product = product_result.scalar_one()

            total_price += product.price * item.count

            new_order = Order(
                id_product=item.id_product,
                id_profile=id_profile,
                count=item.count
            )
            db.add(new_order)
            await db.flush()
            order_ids.append(new_order.id_order)

        order_proc = OrderProcessor(
            id_order=order_ids[0],
            price=total_price,
            count=sum([item.count for item in basket_items]),
            status="создан",
            comment=order_data.comment,
            shipping_cost=order_data.shipping_cost,
            adress=order_data.adress,
            organization=order_data.organization
        )
        db.add(order_proc)

        await db.execute(
            delete(UserBasket).where(UserBasket.id_us_storage.in_(basket_ids))
        )

        await db.commit()
        return order_proc.id_order_proc
