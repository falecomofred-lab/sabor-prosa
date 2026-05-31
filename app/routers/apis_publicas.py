from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from ..services.apis_publicas import APIsPublicas

router = APIRouter(prefix="/api/publicas", tags=["APIs Públicas"])

@router.get("/clima")
async def clima(cidade: str = Query("Niterói")):
    return JSONResponse(await APIsPublicas.previsao_tempo(cidade))

@router.get("/feriados")
async def feriados():
    return JSONResponse(await APIsPublicas.proximos_feriados())

@router.get("/cotacao")
async def cotacao():
    return JSONResponse(await APIsPublicas.cotacao_moedas())

@router.get("/gasolina")
async def gasolina():
    return JSONResponse(await APIsPublicas.preco_gasolina())

@router.get("/rastreio")
async def rastreio(codigo: str = Query(...)):
    return JSONResponse(await APIsPublicas.rastrear_encomenda(codigo))

@router.get("/resumo")
async def resumo():
    return JSONResponse(await APIsPublicas.resumo_diario())
