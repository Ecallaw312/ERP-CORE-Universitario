from fastapi import FastAPI

from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI()


from app.routers import auth, health, module, users

app.include_router(auth.router)
app.include_router(health.router)
app.include_router(module.router)
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"Olá": "API funcionando"}