from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, exists, and_, case, literal_column, func
from apps.user_actions.models import UserAction
from core.models import Product
from apps.user_actions.schema import UserActionOut
from core.models import UserBasket

async def get_user_actions(profile_id: int, action_type: str, session: AsyncSession):
    subquery_in_cart = (
        select(literal_column("1"))
        .select_from(UserBasket)
        .where(
            and_(
                UserBasket.id_product == Product.id_product,
                UserBasket.id_profile == profile_id
            )
        )
    )

    query = (
        select(
            UserAction,
            Product,
            Product.rating,
            Product.id_product,
            case(
                (exists(subquery_in_cart), "true"),
                else_="false"
            ).label("in_cart")
        )
        .join(Product, UserAction.product_id == Product.id_product)
        .filter(UserAction.profile_id == profile_id, UserAction.action == action_type)
    )

    result = await session.execute(query)
    items = result.all()

    return [
        UserActionOut(
            id_product=id_product,
            name_product=product.name_product,
            action_id=action.id_action,
            categories_id=product.categories_id,
            brand=product.brand,
            price=product.price,
            status=product.status,
            img=product.img,
            rating=rating,
            in_cart=in_cart
        )
        for action, product, rating, id_product, in_cart in items
    ]




# async def add_user_action(profile_id: int, product_id: int, action_type: str, session: AsyncSession):
#     action = UserAction(profile_id=profile_id, product_id=product_id, action=action_type)
#     session.add(action)
#     await session.commit()
#     await session.refresh(action)
#     return action

# async def add_user_action(profile_id: int, product_id: int, action_type: str, session: AsyncSession):
#     if action_type == "view":
#         existing_views = await session.execute(
#             select(UserAction)
#             .where(
#                 UserAction.profile_id == profile_id,
#                 UserAction.action == "view"
#             )
#             .order_by(UserAction.date_created.asc())
#         )
#         view_actions = existing_views.scalars().all()
#
#         if len(view_actions) >= 10:
#             to_delete = view_actions[:len(view_actions) - 9]
#             for old_action in to_delete:
#                 await session.delete(old_action)
#
#     action = UserAction(profile_id=profile_id, product_id=product_id, action=action_type)
#     session.add(action)
#     await session.commit()
#     await session.refresh(action)
#     return action

from datetime import datetime
from fastapi import HTTPException
import datetime

async def add_user_action(profile_id: int, product_id: int, action_type: str, session: AsyncSession):
    try:
        if action_type == "view":

            existing_action = await session.execute(
                select(UserAction)
                .where(
                    UserAction.profile_id == profile_id,
                    UserAction.product_id == product_id,
                    UserAction.action == "view"
                )
            )
            existing = existing_action.scalar_one_or_none()

            if existing:

                existing.date_update = datetime.datetime.utcnow()
                await session.commit()
                return {"status": "already_viewed", "action_id": existing.id_action}


            existing_views = await session.execute(
                select(UserAction)
                .where(
                    UserAction.profile_id == profile_id,
                    UserAction.action == "view"
                )
                .order_by(UserAction.date_created.asc())
            )
            view_actions = existing_views.scalars().all()

            if len(view_actions) >= 10:
                to_delete = view_actions[:len(view_actions) - 9]
                for old_action in to_delete:
                    await session.delete(old_action)


        action = UserAction(
            profile_id=profile_id,
            product_id=product_id,
            action=action_type
        )
        session.add(action)
        await session.commit()
        await session.refresh(action)
        return {"status": "added", "action_id": action.id_action}

    except Exception as e:

        raise HTTPException(status_code=400, detail=f"Ошибка при добавлении действия: {str(e)}")





async def delete_favorite(profile_id: int, product_id: int, session: AsyncSession):
    query = delete(UserAction).where(
        UserAction.profile_id == profile_id,
        UserAction.product_id == product_id,
        UserAction.action == "favorite"
    )
    await session.execute(query)
    await session.commit()

