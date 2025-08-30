from dotenv import load_dotenv
from fastapi.routing import APIRoute
import uvicorn
from fastapi import FastAPI
# from app.router import router as appRouter
from starlette.middleware.cors import CORSMiddleware
load_dotenv()

app = FastAPI(
    title="kply_dialysis",
    docs_url="/docs",
    redoc_url="/redoc" ,
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True
    )
