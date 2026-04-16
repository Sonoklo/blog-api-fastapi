from pydantic import BaseModel, Field
from .category import CategoryResponse
from .author import AuthorResponse
from datetime import datetime 
from .paginator import Paginator
class PostBase(BaseModel):
    title:str = Field(
        min_length=5,
        max_length=50,
        description="Уникальное оглавления поста",
        examples=["Новые технологии это-го года"]
    )
    description:str = Field(
        min_length=3, 
        max_length=200,
        description="Описания поста",
        examples=["В этом посте будет расказанно про..."]
    )
    category_id: int = Field(
        description="Уникальный индификатор категорий",
        examples=[1]
    )

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int = Field(
        description="Уникальный индификатор поста",
        examples=[1]
    )
    author: AuthorResponse = Field(
        description="Полная информация автора поста"
    )
    category: CategoryResponse = Field(
        description="Полная информация категории поста"     
    )
    created_at: datetime = Field(
        description="Дата и время создания поста",
    )
    updated_at: datetime = Field(
        description="Дата и время последнего обновления поста",
    )

class AuthorPostResponse(PostBase):
    id: int = Field(
        description="Уникальный индификатор поста",
        examples=[1]
    )
    created_at: datetime = Field(
        description="Уникальный индификатор категории",
        examples=[1]
    )
    updated_at: datetime = Field(
        description="Дата и время последнего обновления поста",
    )

class PostUpdate(PostBase):
    pass

class PaginatedPostResponse(Paginator):
    items: list[PostResponse] = Field(
        description="Лист объектов подробное описующих посты"
    )

class PaginatedAuthorPostResponce(Paginator):
    items: list[AuthorPostResponse] = Field(
        description="Лист объектов подробное описующих посты"
    )