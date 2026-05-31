from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from ..services.evento_inteligente import EventoInteligente

router = APIRouter(prefix="/api/eventos-inteligentes", tags=["Eventos Inteligentes"])

@router.get("/radar")
async def radar_eventos(regiao: str = Query("Niterói")):
    return JSONResponse(await EventoInteligente.buscar_eventos_regiao(regiao))

@router.get("/notificacoes")
async def notificacoes():
    return JSONResponse(await EventoInteligente.gerar_notificacoes())

@router.get("/roi")
async def roi_eventos():
    return JSONResponse(await EventoInteligente.calcular_roi())
