
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from .paginator import Paginator

class AuthorBase(BaseModel):
    email: EmailStr = Field(
        description="Email адрес автора",
        examples=["user@exemple.com"]
    )

    username: str = Field(
        min_length=3,
        max_length=20,
        pattern=r"^[a-zA-Z0-9_-]+$",
        description="Уникальное имя автора",
        examples=["John_Doe", "John-Doe"]
    )

 
class AuthorResponse(AuthorBase):
    id: int = Field(
        description="Уникальный индификатор автора",
        examples=[1]
    )

    created_at: datetime = Field(
        description="Дата и время создания аккаунта",
    )

    
    updated_at: datetime = Field(
        description="Дата и время последнего обновления аккаунта",
    )

class AuthorCreate(AuthorBase):
    password: str = Field(
        min_length=8,
        max_length=25,
        # pattern=r"^(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,25}$",
        description="Пароль (длина 8-25 символов. Должен обязательно содержать 1 большую букву, 1 символ, 1 цифру)",
        examples=["Qwertyu1#"]
    )

class AuthorLogin(BaseModel):
    access_token: str = Field(
        description="JWT токен доступа",
        examples=["vcnbxcvbxcvbx..."]
    )
    token_type: str = Field(
        default="bearer",
        description="Тип токена"
    )

class PaginatedAuthorResponse(Paginator):
    items: list[AuthorResponse] = Field(
        description="Подробное описанния автора"
    )

class TokenData(BaseModel):
    username:str = Field(
        description="Уникальное имя автора",
        examples=["John_Doe", "John-Doe"]
    )