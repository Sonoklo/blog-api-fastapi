from schemas.post import PostCreate, PostResponse, PostUpdate, PaginatedPostResponse, PaginatedAuthorPostResponce
from database import Session
from models.post import Post
from models.author import Author
from models.category import Category
from typing import Optional
from fastapi import HTTPException, status
from .category import get_category_by_id
from sqlalchemy import desc

def create_post(post: PostCreate, db: Session, author: Author) -> PostResponse:
    if get_post_by_title(db, post.title):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Оглавления поста должно быть уникальным")
    category = db.query(Category).filter(Category.id == post.category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Категория не была найдена")

    db_post = Post(**post.model_dump(), author_id=author.id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_posts(db: Session,
            page: int,
            page_size: int,
            author_id: Optional[int] = None,
            category_id: Optional[int] = None,
            title: Optional[str] = None
            ) -> Optional[PaginatedPostResponse]:
    query = db.query(Post).order_by(desc(Post.created_at))
    if author_id:
        query = query.filter(Post.author_id == author_id)
    if category_id:
        query = query.filter(Post.category_id == category_id)
    if title:
        query = query.filter(Post.title == title)
    total = query.count()
    posts = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "items": posts,
        "total_count": total,
        "page": page,
        "page_size": page_size,
        "has_next": page * page_size < total,
        "has_prev": page > 1
    }
    
def get_one_post(post_id:int, db:Session) -> Optional[list[PostResponse]]:
    return form_single_post(get_post_by_id(post_id,db))

def form_post(post: PostResponse) -> dict:
    return {
        "id": post.id,
        "title": post.title,
        "description": post.description,
        "category_id": post.category.id,
        "author": {
            "id": post.author.id,
            "email": post.author.email,
            "username": post.author.username,
            "created_at": post.author.created_at,
            "updated_at": post.author.updated_at,
        },
        "category": {
            "id": post.category.id,
            "title": post.category.title,
            "created_at": post.category.created_at,
            "updated_at": post.category.updated_at,
        },
        "created_at": post.created_at,
        "updated_at": post.updated_at,
    }

def form_post_list(posts: list[PostResponse]) -> list[dict]:
    return [form_post(post) for post in posts]

def form_single_post(post: PostResponse) -> dict:
    return form_post(post)

def get_post_by_title(db:Session, title:str) -> PostResponse:
    return db.query(Post).filter(Post.title == title).first()

def get_author_posts(db: Session,
                    author: Author,
                    page: int,
                    page_size: int,
                    author_id: Optional[int] = None,
                    category_id: Optional[int] = None,
                    title: Optional[str] = None
                    )  -> Optional[PaginatedAuthorPostResponce]:
    query = db.query(Post).filter(Post.author_id == author.id).order_by(desc(Post.created_at))
    if author_id:
        query = query.filter(Post.author_id == author_id)
    if category_id:
        query = query.filter(Post.category_id == category_id)
    if title:
        query = query.filter(Post.title == title)
    total = query.count()
    posts = query.offset((page - 1) * page_size).limit(page_size).all()
    if posts:
        return {
            "items": posts,
            "total_count": total,
            "page": page,
            "page_size": page_size,
            "has_next": page * page_size < total,
            "has_prev": page > 1
        }
    else:
        return None

def get_author_post_by_id(db: Session, post_id:int, author: Author) -> Optional[PostResponse]:
    return db.query(Post).filter(Post.id == post_id, Post.author == author).first()

def get_post_by_id(post_id:int, db:Session) -> Optional[PostResponse]:
    post = db.query(Post).filter(Post.id==post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Нету поста с таким индефикатором")
    else:
        return post
    
def delete_author_post(post_id:int, db:Session, author:Author) -> PostResponse:
    post = get_author_post_by_id(db, post_id, author)
    if post:
        db.delete(post)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Нет поста с таким индефикатором или вы не автор поста")
    
def update_post(post_id:int, new_post: PostUpdate, db: Session, author: Author) -> PostResponse:
    post = get_author_post_by_id(db, post_id, author)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пост не был найден")
    if post.category_id != new_post.category_id:
        category = get_category_by_id(new_post.category_id, db)
        if not category:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Нету категории с таким индефикатором")
    post.title = new_post.title
    post.description = new_post.description
    post.category_id = new_post.category_id
    db.commit()
    db.refresh(post)
    return post
    
        