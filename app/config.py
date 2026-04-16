from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    TITLE:str ="TITLE"
    VERSION:str ="VERSION"
    DESCRIPTION:str ="DESCRIPTION"
    DOCS_URL:str ="/docs"
    OPENAPI_URL: str = "/openapi.json"
    LICENSE_INFO: dict = {
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
    CONTACT_NAME:str = "CONTACT_NAME"
    CONTACT_URL:str = "CONTACT_URL"

    DEBUG: bool = True

    DATABASE_URL:str = "YOUR_DATABASE_URL"
    ECHO:bool = True
    POOL_PRE_PING:bool=True
    POOL_SIZE:int=5
    MAX_OVERFLOW:int=10

    TOKEN_EXPIRES_TIME: int = 0
    SECRET_KEY: str = "YOUR_SECRET_KEY"
    ALGORITHM: str = "ALGORITHM"
@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    return settings

settings = get_settings()