from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..services.radar_service import RadarEventos

router = APIRouter(prefix="/api/radar", tags=["Radar"])

@router.get("/eventos-proximos")
async def eventos_proximos():
    return JSONResponse(await RadarEventos.buscar_eventos_proximos())

@router.get("/sugestoes")
async def sugestoes_busca(regiao: str = "Minas Gerais"):
    return JSONResponse(await RadarEventos.sugerir_eventos_externos(regiao))

@router.get("/oportunidades")
async def verificar_oportunidades():
    return JSONResponse(await RadarEventos.verificar_oportunidades())
