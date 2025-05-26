

from fastapi import APIRouter, HTTPException

from apps.products.models import NewProduct
from apps.products.service import ProductService

router = APIRouter(prefix="/products", tags=["products"])

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


@router.post("/add-product", summary="добавить продукт")
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


@router.get("/all-product/{sort_int}", summary="получить все продукты")
async def get_all_products(sort: int):

    products = await ProductService.select_all_product(sort)

    return products


@router.get("/one-product/{id_product}", summary="получить один продукт")
async def get_one_products(id_product: int):

    products = await ProductService.one_product(id_product)
    return products


@router.get("/del-product/{id_product}", summary="удалить продукт")
async def del_product(id_product: int):

    product = await ProductService.del_product(id_product)

    if product is not None:
        return product
