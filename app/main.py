import uvicorn

from fastapi import FastAPI
from app.endpoints import login, uonetplus_uczen

app = FastAPI(title="Uonetplus API")

app.include_router(login.router)
app.include_router(uonetplus_uczen.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)