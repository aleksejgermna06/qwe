from fastapi import APIRouter, HTTPException, Query, Depends

from apps.products.models import NewProduct, AddProdBask
from apps.products.service import ProductService

from .models import CheckoutOrderRequest
from sqlalchemy.ext.asyncio import AsyncSession
from apps.products.OrderService import OrderService
from core.models import Profile
from core.security import get_async_db, get_current_user,get_current_user_prod

router = APIRouter(prefix="/products", tags=["products"])
router_basket = APIRouter(prefix="/basket", tags=["basket products"])
router_brand = APIRouter(prefix="/brand", tags=["brands of products"])
router_order = APIRouter(prefix="/brand", tags=["brands of order"])
""" @router.get("/HeaderAction", summary="получить все уникальные акции")
async def getHeader():
    try:
        actions = await select_action()
        return [{"action": action} for action in actions]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при получении данных: {str(e)}"
        )  """


@router.post("/product", summary="добавить продукт")
async def add_product(new_Product: NewProduct):
    try:

        product_id = await ProductService.add_product(new_Product)
        if product_id is not None:
            return {
                "status": "success",
                "message": "Продукт успешно добавлен",
                "product_id": product_id,
            }

    except Exception as e:

        raise HTTPException(
            status_code=500, detail=f"Ошибка при добавлении продукта: {str(e)}"
        )


@router.get("/all-product", summary="получить все продукты")
async def get_all_products(sort: int, id_profile: int | None = Query(default=0)):
    products = await ProductService.select_all_product(sort, id_profile)

    return products


@router.get("/filter-product", summary="фильтрация продуктов")
async def get_all_products(page: int = Query(ge=0, default=0),
                           size: int = Query(ge=1, le=100),
                           brand: str | None = Query(default=None, min_length=2, max_length=25),
                           price_filtr: str | None = Query(default=None, min_length=3, max_length=4,
                                                           pattern="^(asc|desc)$", description="Сортировка цены"),
                           popular: str | None = Query(default=None, max_length=4, pattern="^(true)$",
                                                       description="Сортировка по популярности"),
                           min_price: int | None = Query(default=None, description="минимальная цена"),
                           max_price: int | None = Query(default=None, description="максимальная цена"),

                           current_user: Profile = Depends(get_current_user_prod)
                           ):
    products = await ProductService.filter_product(brand, price_filtr, popular, min_price, max_price, page, size,
                                                   current_user.id_profile)

    return products


@router.get("/one-product/{id_product}", summary="получить один продукт")
async def get_one_products(id_product: int,current_user: Profile = Depends(get_current_user_prod) ):
    products = await ProductService.one_product(id_product, current_user.id_profile)
    return products


@router.delete("/product/{id_product}", summary="удалить продукт")
async def del_product(id_product: int):
    product = await ProductService.del_product(id_product)

    if product is not None:
        return product


@router_basket.post("/basket-prod", summary="добавить продукт в корзину")
async def add_prod_bask(id_prod: int, current_user: Profile = Depends(get_current_user)):
    try:

        prod_bask_id = await ProductService.add_product_bask(id_prod, current_user.id_profile)
        if prod_bask_id is not None:
            return {
                "status": "success",
                "message": "Продукт успешно добавлен в корзину",
                "product_id": prod_bask_id,
            }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при добавлении продукта в корзину: {str(e)}",
        )


@router_basket.get("/all-product-bask", summary="получить все продукты")
async def get_all_products(current_user: Profile = Depends(get_current_user),):
    products_bask = await ProductService.sellect_product_bask(current_user.id_profile)

    return products_bask

@router_basket.put("/redact-product-bask", summary="редактирование числа продуктов")
async def put_bask_products(id_prod: int,count:int, current_user: Profile = Depends(get_current_user)):
    products_bask = await ProductService.put_product_bask(id_prod, current_user.id_profile, count)

    if products_bask is not None:
        return {
            "status": "success",
            "message": "номенкулатура изменена",
            "product_id": products_bask,
        }

@router_basket.delete(
    "/del-basket-prod/{id_product}", summary="удалить продукт из корзину"
)
async def del_prod_bask(id_prod: int,  current_user: Profile = Depends(get_current_user)):
    try:

        id_storage = await ProductService.del_product_bask(id_prod, current_user.id_profile)
        if id_storage is not None:
            return {
                "status": "success",
                "message": "номенкулатура удалена",
                "product_id": id_storage,
            }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при удалении номенкулатуры: {str(e)}"
        )


@router_brand.get("/all-brand", summary="получить все бренды")
async def get_all_brand():
    brands = await ProductService.select_brands()
    return brands

from typing import Optional
import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_async_db
from core.security import get_current_user
from core.models import Profile
from .models import CheckoutOrderRequest

router_order = APIRouter()

@router_order.post("/checkout", summary="Оформить заказ")
async def checkout_order(
    order_data: CheckoutOrderRequest,
    current_user: Profile = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    order_proc_id = await OrderService.create_order_with_processor(order_data, current_user.id_profile, db)
    return {
        "status": "success",
        "message": "Заказ успешно оформлен",
        "order_processor_id": order_proc_id
    }


@router_order.get("/orders", summary="Список заказов пользователя")
async def get_user_orders(
    current_user: Profile = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    orders = await OrderService.get_orders_by_user(current_user.id_profile, db)
    return {"orders": orders}




@router.get("/serch", summary="поиск категорий и продуктов")
async def serch(litters: str):
    res = await ProductService.serch(litters)
    return res