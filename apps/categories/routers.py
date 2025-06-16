from fastapi import APIRouter, Query

from apps.categories.service import CategorieService, heder
from apps.categories.models import NewCatProdCom
router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/header-categories", summary="получить все для хедера")
async def get_all_hed():
    hed = await heder()
    return hed


@router.get("/all-cat/{sort}", summary="получить все категории")
async def get_all_cat(sort: int):

    cats = await CategorieService.select_all_cat(sort)

    return cats


@router.get("/one-cat", summary="получить одну категории")
async def get_one_cat(url: str, id_profile: int | None = Query(default=0)):

    cats = await CategorieService.select_one_cat(url, id_profile)

    return cats

@router.get("/user-cat-comparison/{id_profile}", summary="получить категории для сравнения")
async def get_cat_comparison(id_profile: int):

    cats = await CategorieService.select_cat_comparison(id_profile)

    return cats
@router.get("/user-cat-prods-comparison", summary="получить продукты для сравнения")
async def get_cat_prod_comparison(
                                id_profile: int,
                                id_cat: int,
                            ):

    cats = await CategorieService.select_cat_prod_comparison(id_profile, id_cat)

    return cats

@router.post("/cat-comparison", summary="добавить продукт для сравнения")
async def add_cat_comparison(AddCatProdCom: NewCatProdCom):

    cats = await CategorieService.add_product_comsommer(AddCatProdCom)

    return {
                "status": "success",
                "message": "Продукт успешно добавлен",
                "product_id": cats,
            }
    