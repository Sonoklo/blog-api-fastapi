from sqlalchemy.orm import Session
from models.author import Author
from schemas.author import PaginatedAuthorResponse
from typing import Optional
from core.security import get_password_hash, verify_password
import datetime
from jose import jwt
from config import settings
from sqlalchemy import  desc
from fastapi import HTTPException

def get_by_email(db: Session, email: str) -> Optional[Author]:
    return db.query(Author).filter(Author.email == email).first()

def get_by_username(db: Session, username: str) -> Optional[Author]:
    return db.query(Author).filter(Author.username == username).first()


def get_author(db:Session, username:str, password:str) -> Optional[Author]:
    author:Author = get_by_username(db, username)
    if not author:
        return None

    if not verify_password(password,author.password):
        return None
    
    return author
 

def get_all_authors(db:Session, page:int, page_size:int) -> Optional[PaginatedAuthorResponse]:
    query = db.query(Author).order_by(desc(Author.created_at))
    total = query.count()
    if (page - 1) * page_size >= total and total != 0:
        raise HTTPException(404, "Страница не найденна")
    author = query.offset((page - 1) * page_size).limit(page_size).all()
    if author:
        return {
            "items": author,
            "total_count": total,
            "page": page,
            "page_size": page_size,
            "has_next": page * page_size < total,
            "has_prev": page > 1
        }
    else:
        None

def create(db: Session, author: Author) -> Author:
    hash_password = get_password_hash(author.password)
    db_author = Author(email = author.email, username = author.username, password=hash_password)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def create_access_token(data: dict["sub":str, "user_id": int, "exp":datetime.timedelta]) -> str:
    data["exp"] = datetime.datetime.now() + data["exp"]
    token = jwt.encode(data, settings.SECRET_KEY, settings.ALGORITHM)
    return token

def verify_access_token(token:str) -> Optional[dict]:
    try:
        data = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        return data
    except:
        return None