from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..services.gatilho_service import GatilhoService

router = APIRouter(prefix="/api/gatilhos", tags=["Gatilhos"])

@router.get("/reposicao")
async def gatilhos_reposicao():
    """Clientes que podem precisar de reposição (20+ dias)."""
    return JSONResponse(GatilhoService.verificar_reposicao())

@router.get("/inativos")
async def gatilhos_inativos():
    """Clientes inativos há mais de 30 dias."""
    return JSONResponse(GatilhoService.verificar_clientes_inativos())

@router.get("/aniversario")
async def gatilhos_aniversario():
    """Clientes aniversariantes do mês."""
    return JSONResponse(GatilhoService.clientes_aniversariantes())
