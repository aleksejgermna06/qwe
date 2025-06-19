from fastapi import APIRouter, Query,Depends
from core.security import get_current_user,get_current_user_prod
from apps.categories.service import CategorieService, heder
from core.models import Profile
from apps.categories.schema import CatComOut, CatProdOut
from typing import List, Literal
router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/header-categories", summary="получить все для хедера")
async def get_all_hed():
    hed = await heder()
    return hed


@router.get("/all-cat/{sort}", summary="получить все категории")
async def get_all_cat(sort: int):

    cats = await CategorieService.select_all_cat(sort)

    return cats

""" @router.get("/{action_type}", response_model=List[UserActionOut])
async def get_actions(
    action_type: Literal["favorite", "view"],
    current_user: Profile = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    return await get_user_actions(current_user.id_profile, action_type, db) """

@router.get("/one-cat", summary="получить одну категории")
async def get_one_cat(url: str, current_user: Profile = Depends(get_current_user_prod)):

    cats = await CategorieService.select_one_cat(url, current_user.id_profile)

    return cats


@router.get("/user-cat-comparison", summary="получить категории для сравнения", response_model=List[CatComOut])
async def get_cat_comparison(current_user: Profile = Depends(get_current_user),):

    cats = await CategorieService.select_cat_comparison(current_user.id_profile)

    return cats
@router.get("/user-cat-prods-comparison/{url}", summary="получить продукты для сравнения",response_model=List[CatProdOut])
async def get_cat_prod_comparison(
                                url: str,
                                current_user: Profile = Depends(get_current_user),
                            ):

    #cats = await CategorieService.select_cat_prod_comparison(current_user.id_profile, id_cat)

    return await CategorieService.select_cat_prod_comparison(current_user.id_profile, url)

@router.post("/cat-comparison", summary="добавить продукт для сравнения")
async def add_cat_comparison(product_id: int, current_user: Profile = Depends(get_current_user)):

    cats = await CategorieService.add_product_comsommer(current_user.id_profile, product_id)

    return {
                "status": "success",
                "message": "Продукт успешно добавлен",
                "product_id": cats,
            }
    
@router.delete("/del-prod-comparison/{id_product}", summary="удалить продукт из сравнения")
async def del_cat_comparison(
                                id_product: int,
                                current_user: Profile = Depends(get_current_user),
                            ):

    cats = await CategorieService.del_product_comp( id_product, current_user.id_profile)

    return {
                "status": "success",
                "message": "Продукт успешно удален",
                "product_id": cats,
            }

@router.delete("/del-cat-comparison/{url}", summary="удалить продукт из сравнения")
async def del_cat_comparison(
                                url: str,
                                current_user: Profile = Depends(get_current_user),
                            ):

    cats = await CategorieService.del_cat_comp( url, current_user.id_profile)

    return {
                "status": "success",
                "message": "Продукт успешно удален",
                "url": cats,
            }