from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..services.monitor_service import MonitorPrecos

router = APIRouter(prefix="/api/monitor", tags=["Monitor"])

@router.get("/produtos")
async def listar_produtos():
    return JSONResponse(await MonitorPrecos.listar_produtos_monitorados())

@router.get("/alertas")
async def verificar_alertas():
    return JSONResponse(await MonitorPrecos.verificar_alertas_precos())

@router.get("/fornecedores")
async def fornecedores_alternativos():
    return JSONResponse(await MonitorPrecos.sugerir_fornecedores_alternativos())
