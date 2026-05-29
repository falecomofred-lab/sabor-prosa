from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from ..services.pedido_service import PedidoService

router = APIRouter(prefix="/api/pedido", tags=["Pedido"])

@router.post("/gerar")
async def gerar_pedido(request: Request):
    """Gera pedido de compra inteligente usando IA (Curva ABC)."""
    service = PedidoService()
    resultado = await service.gerar_pedido_inteligente()
    return JSONResponse(resultado)
