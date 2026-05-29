from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..services.roteiro_service import RoteiroService

router = APIRouter(prefix="/api/roteiros", tags=["Roteiros"])

@router.get("/estoque-parado")
async def analisar_estoque():
    service = RoteiroService()
    result = await service.analisar_estoque_parado()
    return JSONResponse(result)

@router.post("/video")
async def gerar_roteiro(data: dict):
    service = RoteiroService()
    result = await service.gerar_roteiro_video(
        produto_nome=data.get("produto_nome", ""),
        produto_desc=data.get("produto_desc", ""),
        preco=data.get("preco", 0)
    )
    return JSONResponse(result)

@router.get("/combo")
async def gerar_combo():
    service = RoteiroService()
    result = await service.gerar_combo_promocional()
    return JSONResponse(result)
