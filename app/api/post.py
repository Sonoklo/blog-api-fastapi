from typing import Optional

from fastapi import APIRouter, status, Depends, Query, Path
from schemas.post import PostCreate, PostResponse,PostUpdate, PaginatedPostResponse, PaginatedAuthorPostResponce
from database import Session, get_db
import crud.post as crud
from models.author import Author
from core.dependencies import get_current_user

router_author_post = APIRouter(
    prefix="/posts",
    tags=["Автор", "Посты"]
)

router_post = APIRouter(
    prefix="/posts",
    tags=["Посты"]
)
@router_author_post.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def publish_post(post: PostCreate, db:Session=Depends(get_db), author: Author = Depends(get_current_user)):
    return crud.create_post(post,db, author)

@router_post.get("",response_model=PaginatedPostResponse, status_code=status.HTTP_200_OK)
def get_posts_route(page: int = Query(1,ge=1, description="Номер странички (начинается с 1)"), 
                    page_size: int = Query(10,ge=1, le=100, description="Количество элементов на страничке"), 
                    author_id: Optional[int] = Query(None, ge=1,description="Фильтр по ID автора"),
                    category_id: Optional[int] = Query(None, ge=1, description="Фильтр по ID категории"),
                    title: Optional[str] = Query(None, ge=1, description="Фильтр по заголовку"),
                    db: Session = Depends(get_db)):
    result = crud.get_posts(db,page,page_size,author_id,category_id,title)
    posts = result["items"]
    result["items"] = crud.form_post_list(posts)
    return result

@router_post.get("/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK)
def get_post(   post_id: int = Path(gt=0, description="Индефикатор поста"),
                db:Session=Depends(get_db)):
    return crud.get_one_post(post_id, db)

@router_author_post.get("/me", response_model=PaginatedAuthorPostResponce, status_code=status.HTTP_200_OK)
def get_author_post(page: int = Query(1,ge=1, description="Номер странички (начинается с 1)"), 
                    page_size: int = Query(10,ge=1, le=100, description="Количество элементов на страничке"), 
                    author_id: Optional[int] = Query(None,description="Фильтр по ID автора"),
                    category_id: Optional[int] = Query(None, description="Фильтр по ID категории"),
                    title: Optional[str] = Query(None, description="Фильтр по заголовку"),
                    db: Session = Depends(get_db),
                    author: Author = Depends(get_current_user)):
    return crud.get_author_posts(db,author,page,page_size,author_id,category_id,title)

@router_author_post.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author_post( post_id: int = Path(gt=0, description="Идентификатор поста"),
                        db:Session=Depends(get_db),
                        author: Author = Depends(get_current_user)):
    crud.delete_author_post(post_id, db, author)

@router_author_post.put("/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK)
def put_author_post(new_post:PostUpdate,
                    post_id: int = Path(gt=0, description="Идентификатор поста"),
                    db:Session=Depends(get_db),
                    author: Author = Depends(get_current_user)):
    return crud.update_post(post_id, new_post, db, author)

