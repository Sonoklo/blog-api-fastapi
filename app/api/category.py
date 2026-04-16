from fastapi import APIRouter, status, Depends, Query, Path
from database import Session, get_db
import crud.category as crud
from schemas.category import CategoryResponse,CategoryBase,CategoryPaginatedResponse,CategoryUpdate
from models.author import Author
from core.dependencies import get_current_user

router_category = APIRouter(
    prefix="/category",
    tags=["Категории"]
)

@router_category.post("/create", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category:CategoryBase, db:Session=Depends(get_db), author: Author = Depends(get_current_user)):
    return crud.create_category(category, db)

@router_category.get("", response_model=CategoryPaginatedResponse, status_code=status.HTTP_200_OK)
def get_all_categories( page: int = Query(1,ge=1, description="Номер странички (начинается с 1)"), 
                        page_size: int = Query(10,ge=1, le=100, description="Количество элементов на страничке"),
                        db:Session=Depends(get_db)):
    return crud.get_categories(page,page_size,db)

@router_category.get("/{category_id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
def get_category(category_id:int = Path(gt=0, description="Индентификатор категории"),
                 db:Session=Depends(get_db)):
    return crud.get_category_by_id(category_id, db)

@router_category.put("/{category_id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
def update_category(new_category:CategoryUpdate,
                    category_id:int = Path(gt=0, description="Индентификатор категории"),
                    db:Session=Depends(get_db)):
    return crud.create_new_category(category_id,new_category,db)

@router_category.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_category(category_id:int = Path(gt=0, description="Индентификатор категории"),
                    db:Session=Depends(get_db)):
    crud.delete_category(category_id,db)