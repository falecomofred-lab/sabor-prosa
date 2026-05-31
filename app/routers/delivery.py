from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from ..services.delivery_service import DeliveryService

router = APIRouter(prefix="/api/delivery", tags=["Delivery"])

@router.get("/cotar")
async def cotar_entrega(
    origem: str = Query("24000-000"),
    destino: str = Query("24000-001"),
    peso: float = Query(2.0)
):
    """Cotar frete com serviços de moto delivery."""
    resultado = await DeliveryService.cotar_entrega(origem, destino, peso)
    return JSONResponse(resultado)

@router.post("/solicitar")
async def solicitar_entrega(data: dict):
    """Solicitar entrega por motoboy."""
    resultado = await DeliveryService.solicitar_entrega(
        servico=data.get("servico", "99Entregas"),
        origem=data.get("origem", ""),
        destino=data.get("destino", ""),
        contato_origem=data.get("contato_origem", ""),
        contato_destino=data.get("contato_destino", ""),
        descricao=data.get("descricao", "Alimentos perecíveis")
    )
    return JSONResponse(resultado)
