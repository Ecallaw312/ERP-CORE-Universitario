from fastapi import FastAPI

app = FastAPI()

from app.routers import router

app.include_router(router)

@app.get("/")
def read_root():
    return {"Olá": "API funcionando"}