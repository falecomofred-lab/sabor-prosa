from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..services.video_service import VideoService
from ..services.agente_conteudo import AgenteConteudo

router = APIRouter(prefix="/api/conteudo", tags=["Conteudo"])

@router.post("/gerar-video")
async def gerar_video(data: dict):
    service = VideoService()
    result = await service.gerar_video(
        produto_nome=data.get("produto_nome", ""),
        produto_desc=data.get("produto_desc", ""),
        foto_path=data.get("foto_path", "")
    )
    return JSONResponse(result)

@router.post("/gerar-post")
async def gerar_post(data: dict):
    agente = AgenteConteudo()
    result = await agente.gerar_post(
        tipo=data.get("tipo", "produto_dia"),
        produto_nome=data.get("produto_nome", ""),
        produto_desc=data.get("produto_desc", ""),
        preco=data.get("preco", 0)
    )
    return JSONResponse(result)
