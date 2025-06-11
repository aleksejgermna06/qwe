

from fastapi import APIRouter, HTTPException, Query

from apps.products.models import NewProduct, AddProdBask
from apps.products.service import ProductService

router = APIRouter(prefix="/products", tags=["products"])
router_basket = APIRouter(prefix="/basket", tags=["basket products"])
router_brand = APIRouter(prefix="/brand", tags=["brands of products"])
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


@router.get("/all-product/{sort}", summary="получить все продукты")
async def get_all_products(sort: int):

    products = await ProductService.select_all_product(sort)

    return products

@router.get("/filter-product", summary="фильтрация продуктов")
async def get_all_products(brand:str | None = Query(default=None, min_length=2, max_length=25),                        
                           price_filtr:str | None = Query(default=None, min_length=3, max_length=4, pattern="^(asc|desc)$",  description="Сортировка цены"),
                           popular:str | None = Query(default=None, max_length=4, pattern="^(true)$",description="Сортировка по популярности"),
                           min_price:int | None = Query(default=None,  description="минимальная цена"),
                           max_price:int | None = Query(default=None,  description="максимальная цена"),
                           ):


    products = await ProductService.filter_product(brand,price_filtr,popular,min_price,max_price)
    return products


@router.get("/one-product/{id_product}", summary="получить один продукт")
async def get_one_products(id_product: int):

    products = await ProductService.one_product(id_product)
    return products


@router.delete("/product/{id_product}", summary="удалить продукт")
async def del_product(id_product: int):

    product = await ProductService.del_product(id_product)

    if product is not None:
        return product

@router_basket.post("/basket-prod", summary="добавить продукт в корзину")
async def add_prod_bask( add_prod_bask : AddProdBask):
   
    try:

        prod_bask_id = await ProductService.add_product_bask(add_prod_bask)
        if prod_bask_id is not None:
            return {
                "status": "success",
                "message": "Продукт успешно добавлен в корзину",
                "product_id": prod_bask_id,
            }

    except Exception as e:

        raise HTTPException(
            status_code=500, detail=f"Ошибка при добавлении продукта в корзину: {str(e)}"
        )
    
@router_basket.get("/all-product-bask/{id_user}", summary="получить все продукты")
async def get_all_products(id_user: int):

    products_bask = await ProductService.sellect_product_bask(id_user)

    return products_bask

@router_basket.delete("/basket-prod/{id_us_storage}", summary="удалить продукт из корзину")
async def del_prod_bask( id_us_storage: int):
    try:

        id_storage = await ProductService.del_product_bask(id_us_storage)
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
   

    brands=await ProductService.select_brands()
    return brands
