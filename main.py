import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from cryptography.fernet import Fernet
from app.routes import auth, uonetplus_uczen, github
from app.core.config import settings

app = FastAPI(title="Uonetplus API", version="0.3.0")

app.include_router(auth.router, prefix=settings.API_V1_URL + "/auth", tags=["auth"])
app.include_router(uonetplus_uczen.router, prefix=settings.API_V1_URL + "/uonetplus-uczen", tags=["uonetplus-uczen"])
app.include_router(github.router, prefix=settings.API_V1_URL + "/github", tags=["github"])

secret_key = Fernet.generate_key().decode("utf-8")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=secret_key)

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.API_HOST, port=settings.API_PORT, reload=True)
