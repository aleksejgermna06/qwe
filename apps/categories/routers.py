from fastapi import APIRouter

from apps.categories.service import CategorieService, heder

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/header-categories", summary="получить все для хедера")
async def get_all_hed():
    hed = await heder()
    return hed


@router.get("/all-cat/{sort}", summary="получить все категории")
async def get_all_cat(sort: int):

    cats = await CategorieService.select_all_cat(sort)

    return cats


@router.get("/one-cat/{url}", summary="получить одну категории")
async def get_one_cat(url: str):

    cats = await CategorieService.select_one_cat(url)

    return cats
