from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from ..services.qrcode_service import QRCodeService

router = APIRouter(prefix="/api/qrcode", tags=["QRCode"])

@router.post("/gerar")
async def gerar_qrcode(data: dict):
    """Gera QR Code personalizado."""
    url = data.get("url", "http://localhost:8000/cadastro-evento")
    tipo = data.get("tipo", "normal")
    
    if tipo == "cartaz":
        caminho = QRCodeService.gerar_qrcode_para_impressao(
            url=url,
            titulo=data.get("titulo", "Sabor e Prosa Empório"),
            subtitulo=data.get("subtitulo", "Escaneie e cadastre-se!")
        )
    else:
        caminho = QRCodeService.gerar_qrcode_personalizado(url=url)
    
    return JSONResponse({"sucesso": True, "caminho": caminho, "url": url})

@router.get("/baixar")
async def baixar_qrcode(arquivo: str = Query(...)):
    """Download do QR Code gerado."""
    caminho = f"app/static/qrcodes/{arquivo}"
    return FileResponse(caminho, media_type="image/png", filename=arquivo)
