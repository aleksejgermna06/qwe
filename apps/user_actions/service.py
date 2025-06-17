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

