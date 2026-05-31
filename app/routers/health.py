from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencia import get_db, verificar_token
from app.models.module import Modulo_db
import httpx
import asyncio
from app.models.user import User_db

router = APIRouter(tags=["Health"])

async def checar_modulo(nome: str, url: str, porta: int) -> tuple[str, str]:
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            response = await client.get(f"{url}:{porta}/health")
            if response.status_code == 200:
                return nome, "online"
            return nome, "offline"
    except Exception:
        return nome, "offline"

@router.get("/health")
async def health(session: Session = Depends(get_db)):
    modulos = session.query(Modulo_db).filter(Modulo_db.ativo == True).all()

    tarefas = [
        checar_modulo(m.nome, m.url, m.porta)
        for m in modulos
    ]

    resultados = await asyncio.gather(*tarefas)

    services = {"core": "online"}
    for nome, status in resultados:
        services[nome] = status

    status_geral = "ok" if all(s == "online" for s in services.values()) else "degraded"

    return {
        "status": status_geral,
        "services": services
    }