


from fastapi import APIRouter, status, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordRequestForm
from schemas.author import *
from sqlalchemy.orm import Session
from database import get_db
import crud.author as crud_author
from datetime import timedelta
from config import settings
from models.author import Author
from core.dependencies import get_current_user

router_auth = APIRouter(
    prefix="/author",
    tags=["Аутентификация", "Автор"]
)


router_author = APIRouter(
    prefix="/author",
    tags=["Автор"]
)

router_authors = APIRouter(
    prefix = "/authors",
    tags=["Автор"]
)

@router_auth.post("/register",response_model=AuthorResponse, status_code=status.HTTP_201_CREATED)
def register(author: AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud_author.get_by_email(db,email=author.email)
    if db_author:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Автор с такой електронной почтой уже существует")

    db_author = crud_author.get_by_username(db,username=author.username)
    if db_author:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Автор с таким юзернеймом уже существует")
    
    return crud_author.create(db,author=author)

@router_auth.post("/login",response_model=AuthorLogin,status_code=status.HTTP_200_OK)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db:Session=Depends(get_db)):
    db_author = crud_author.get_author(db, username=form_data.username, password=form_data.password)
    if db_author:
        access_token_expires = timedelta(minutes=settings.TOKEN_EXPIRES_TIME)
        token = crud_author.create_access_token(
            data={"sub": db_author.username, "user_id": db_author.id, "exp":access_token_expires},
        )
        return {"access_token": token}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный логин или пароль")


@router_authors.get("", response_model=PaginatedAuthorResponse)
def get_authors(page: int = Query(1,ge=1, description="Номер странички (начинается с 1)"), 
                page_size: int = Query(10,ge=1, le=100, description="Количество элементов на страничке"), 
                db:Session=Depends(get_db)):
    result = crud_author.get_all_authors(db, page, page_size)
    return result

@router_authors.get("/me", response_model=AuthorResponse)
def get_author_info(author: Author = Depends(get_current_user)):
    return author
