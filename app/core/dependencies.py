

from fastapi.security import OAuth2PasswordBearer
from models.author import Author
from fastapi import Depends, HTTPException, status
from typing import Optional
from database import Session, get_db
from crud.author import verify_access_token
from schemas.author import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/author/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Author:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = verify_access_token(token)
    if payload is None:
        raise credentials_exception
    
    username: Optional[str] = payload.get("sub")
    if username is None:
        raise credentials_exception
    
    token_data = TokenData(username=username)
    
    user = db.query(Author).filter(Author.username == token_data.username).first()
    if user is None:
        raise credentials_exception

    return user