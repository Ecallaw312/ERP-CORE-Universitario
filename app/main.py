from fastapi import FastAPI

app = FastAPI()
from app.routers import auth

app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"Olá": "API funcionando"}