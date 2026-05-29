from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from anthropic import Anthropic
from ..config import get_settings
from ..database import SessionLocal

settings = get_settings()
router = APIRouter(prefix="/api/caixa", tags=["Caixa"])

@router.post("/fechamento")
async def fechamento_caixa(request: Request):
    """Recebe valores do fechamento e compara com PDV. IA analisa divergências."""
    try:
        dados = await request.json()
        dinheiro_informado = float(dados.get("dinheiro", 0))
        cartao_informado = float(dados.get("cartao", 0))
        pix_informado = float(dados.get("pix", 0))
        
        total_informado = dinheiro_informado + cartao_informado + pix_informado
        total_registrado = 2500.00  # Placeholder - virá do banco real de vendas
        
        diferenca = round(total_informado - total_registrado, 2)
        
        resultado = {
            "total_informado": total_informado,
            "total_registrado": total_registrado,
            "diferenca": diferenca,
            "status": "ok" if abs(diferenca) < 10 else "divergencia",
            "diagnostico": ""
        }
        
        # Se houver divergência > R, IA analisa
        if abs(diferenca) >= 10:
            client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            prompt = f"""Analise o fechamento de caixa do Sabor e Prosa Empório:

Total registrado no PDV: R$ {total_registrado:.2f}
Total informado pelo lojista: R$ {total_informado:.2f}
Diferença: R$ {diferenca:.2f} ({'sobrando' if diferenca > 0 else 'faltando'})

Possíveis causas para investigar:
1. Erro de troco em alguma venda
2. Venda pausada (Hold Sale) não finalizada
3. Esquecimento de registrar alguma despesa

Dê um diagnóstico curto e amigável (tom mineiro, use 'trem', 'uai', 'sô') com sugestão do que revisar. Máximo 3 frases."""
            
            message = client.messages.create(
                model=settings.AI_MODEL,
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )
            resultado["diagnostico"] = message.content[0].text
        
        return JSONResponse(resultado)
    except Exception as e:
        return JSONResponse({"erro": str(e)}, status_code=500)
