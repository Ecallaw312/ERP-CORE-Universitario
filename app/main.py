from fastapi import FastAPI
app = FastAPI()

import app.routers

app.include_router(app.routers.auth.router) 
app.include_router(app.routers.health.router) 
app.include_router(app.routers.module.router)
app.include_router(app.routers.users.router)


@app.get("/")
def read_root():
    return {"Olá": "API funcionando"}