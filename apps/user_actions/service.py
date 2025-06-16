from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from apps.user_actions.models import UserAction
from core.models import Product
from apps.user_actions.schema import UserActionOut


async def get_user_actions(profile_id: int, action_type: str, session: AsyncSession):
    query = (
        select(UserAction, Product)
        .join(Product, UserAction.product_id == Product.id_product)
        .filter(UserAction.profile_id == profile_id, UserAction.action == action_type)
    )
    result = await session.execute(query)
    items = result.all()

    return [
        UserActionOut(
            name_product=product.name_product,
            action_id=action.id_action,
            categories_id=product.categories_id,
            brand=product.brand,
            price=product.price,
            status=product.status,
            img=product.img
        )
        for action, product in items
    ]


async def add_user_action(profile_id: int, product_id: int, action_type: str, session: AsyncSession):
    action = UserAction(profile_id=profile_id, product_id=product_id, action=action_type)
    session.add(action)
    await session.commit()
    await session.refresh(action)
    return action


async def delete_favorite(profile_id: int, product_id: int, session: AsyncSession):
    query = delete(UserAction).where(
        UserAction.profile_id == profile_id,
        UserAction.product_id == product_id,
        UserAction.action == "favorite"
    )
    await session.execute(query)
    await session.commit()

