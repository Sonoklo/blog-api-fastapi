from pydantic import BaseModel, Field

class Paginator(BaseModel):
    
    total_count: int = Field(
        description = "Полное количество страниц",
        examples=[10]
    )
    page: int  = Field(
        description = "Текущая страница",
        examples=[1]
    )
    page_size: int  = Field(
        description = "Количество постов на странице",
        examples=[5]
    )
    has_next: bool  = Field(
        description = "Есть ли следующая страница постов",
        examples=[True, False]
    )
    has_prev: bool  = Field(
        description = "Есть ли предыдущая страница постов",
        examples=[True, False]
    )