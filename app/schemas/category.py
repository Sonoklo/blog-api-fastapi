from pydantic import BaseModel, Field
from .paginator import Paginator
from datetime import datetime

class CategoryBase(BaseModel):
    title:str = Field(
        min_length=5,
        max_length=50,
        description="Уникальное названия категории",
        examples=["Технологии"]
    )

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int =  Field(
        description="Уникальный индификатор поста",
        examples=[1]
    )
    created_at: datetime = Field(
        description="Дата и время создания категории",
    )
    updated_at: datetime = Field(
        description="Дата и время последнего обновления категории",
    )
    
class CategoryPaginatedResponse(Paginator):
    items: list[CategoryResponse]= Field(
        description="Лист объектов подробное описующих категории"
    )