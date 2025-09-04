from dotenv import load_dotenv
from fastapi.routing import APIRoute
import uvicorn
from fastapi import FastAPI
from core.config import settings
from starlette.middleware.cors import CORSMiddleware
load_dotenv()
from app.api import router as routes


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc" ,
)

app.include_router(routes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
    expose_headers=settings.CORS_EXPOSE_HEADERS,
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT, 
        reload=True,
    )




