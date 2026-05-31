from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.routers import auth, health, module, users

app.include_router(auth.router)
app.include_router(health.router)
app.include_router(module.router)
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"Olá": "API funcionando"}