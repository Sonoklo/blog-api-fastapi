from fastapi import HTTPException, status
from schemas.category import CategoryBase,CategoryPaginatedResponse,CategoryUpdate
from database import Session
from models.category import Category
from sqlalchemy import desc
from typing import Optional

def create_category(category:CategoryBase, db:Session) -> Category:
    exist_category = get_category_by_title(category.title, db)
    if exist_category:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Оглавления категории должно быть уникальным")
    db_category = Category(title=category.title)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories(page:int,page_size:int,db:Session) -> Optional[CategoryPaginatedResponse]:
    query = db.query(Category).order_by(desc(Category.created_at))
    total = query.count()
    if (page - 1) * page_size >= total and total != 0:
        raise HTTPException(404, "Страница не найденна")
    categories = query.offset((page - 1) * page_size).limit(page_size).all()
    if categories:
        return {
            "items": categories,
            "total_count": total,
            "page": page,
            "page_size": page_size,
            "has_next": page * page_size < total,
            "has_prev": page > 1
        }
    else:
        return None

def get_category_by_id(category_id:int, db:Session) -> Category:
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Категория не была найдена")
    return category

def get_category_by_title(title:str, db:Session) -> Category:
    category = db.query(Category).filter(Category.title == title).first()
    return category

def create_new_category(category_id:int, new_category:CategoryUpdate,db:Session) -> Category:
    category = get_category_by_id(category_id,db)
    category.title = new_category.title
    db.commit()
    db.refresh(category)
    return category

def delete_category(category_id: int, db: Session):
    category = get_category_by_id(category_id, db)
    db.delete(category)
    db.commit()