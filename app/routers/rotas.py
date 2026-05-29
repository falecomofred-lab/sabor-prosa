from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..services.roteirizador_service import RoteirizadorService

router = APIRouter(prefix="/api/rotas", tags=["Rotas"])

@router.get("/entregas")
async def listar_entregas():
    return JSONResponse(await RoteirizadorService.listar_entregas_pendentes())

@router.get("/otimizar")
async def otimizar_rota():
    entregas = await RoteirizadorService.listar_entregas_pendentes()
    resultado = await RoteirizadorService.otimizar_rota(entregas)
    return JSONResponse(resultado)

@router.get("/resumo")
async def resumo_diario():
    return JSONResponse(await RoteirizadorService.gerar_resumo_entrega())
