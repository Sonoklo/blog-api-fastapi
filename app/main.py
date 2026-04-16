from fastapi import FastAPI
from config import settings
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import init_db
from api import author, post, category

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Start FAST API application")
    init_db()
    yield
    print("Shutdown FAST API application")

app = FastAPI(
    title=settings.TITLE,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    docs_url=settings.DOCS_URL,
    lifespan=lifespan,
    openapi_url=settings.OPENAPI_URL,
    license_info=settings.LICENSE_INFO,
    contact={
        "name": settings.CONTACT_NAME,
        "url": settings.CONTACT_URL
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],                                     
    allow_credentials=True,                              
    allow_methods=["GET", "POST", "DELETE", "PUT"],       
    allow_headers=["*"]                                  


app.include_router(author.router_auth)
app.include_router(author.router_author)
app.include_router(post.router_author_post)
app.include_router(post.router_post)
app.include_router(category.router_category)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )