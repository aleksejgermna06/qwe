from fastapi import APIRouter, Query,Depends
from core.security import get_current_user
from apps.categories.service import CategorieService, heder
from core.models import Profile
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

""" @router.get("/{action_type}", response_model=List[UserActionOut])
async def get_actions(
    action_type: Literal["favorite", "view"],
    current_user: Profile = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    return await get_user_actions(current_user.id_profile, action_type, db) """

@router.get("/one-cat", summary="получить одну категории")
async def get_one_cat(url: str, id_profile: int | None = Query(default=0)):

    cats = await CategorieService.select_one_cat(url, id_profile)

    return cats


@router.get("/user-cat-comparison", summary="получить категории для сравнения")
async def get_cat_comparison(current_user: Profile = Depends(get_current_user),):

    cats = await CategorieService.select_cat_comparison(current_user.id_profile)

    return cats
@router.get("/user-cat-prods-comparison", summary="получить продукты для сравнения")
async def get_cat_prod_comparison(
                                id_cat: int,
                                current_user: Profile = Depends(get_current_user),
                            ):

    cats = await CategorieService.select_cat_prod_comparison(current_user.id_profile, id_cat)

    return cats

@router.post("/cat-comparison", summary="добавить продукт для сравнения")
async def add_cat_comparison(AddCatProdCom: NewCatProdCom):

    cats = await CategorieService.add_product_comsommer(AddCatProdCom)

    return {
                "status": "success",
                "message": "Продукт успешно добавлен",
                "product_id": cats,
            }
    
@router.delete("/del-cat-comparison", summary="удалить продукт из сравнения")
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
