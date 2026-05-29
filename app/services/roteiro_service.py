from anthropic import Anthropic
from ..config import get_settings
from ..database import SessionLocal
from ..models import Produto
from datetime import datetime

settings = get_settings()

class RoteiroService:
    def __init__(self):
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    
    async def analisar_estoque_parado(self) -> dict:
        """Analisa produtos com estoque alto e sugere promoções."""
        db = SessionLocal()
        produtos = db.query(Produto).filter(Produto.estoque_atual >= 15).order_by(Produto.estoque_atual.desc()).limit(5).all()
        db.close()
        
        if not produtos:
            return {"sugestoes": [], "mensagem": "Estoque equilibrado! ✅"}
        
        prompt = f"""Analise o estoque do empório e sugira ações:

PRODUTOS COM ESTOQUE ALTO:
{chr(10).join([f'- {p.nome}: {p.estoque_atual} unidades (Preço: R$ {p.preco_venda:.2f})' for p in produtos])}

Sugira:
1. Um combo promocional com 2-3 produtos
2. Um roteiro de vídeo de 30 segundos para Reels/TikTok
3. Um texto para post no Instagram
4. Uma mensagem para WhatsApp dos clientes

Formato: TÍTULO | CONTEÚDO para cada item."""
        
        message = self.client.messages.create(
            model=settings.AI_MODEL,
            max_tokens=600,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return {
            "sugestoes": [
                {"produto": p.nome, "estoque": p.estoque_atual, "preco": p.preco_venda}
                for p in produtos
            ],
            "analise_ia": message.content[0].text
        }
    
    async def gerar_roteiro_video(self, produto_nome: str, produto_desc: str, preco: float) -> dict:
        """Gera roteiro detalhado para vídeo curto."""
        prompt = f"""Crie um roteiro de 30 segundos para Reels/TikTok divulgando:

Produto: {produto_nome}
Descrição: {produto_desc}
Preço: R$ {preco:.2f}

Formato:
CENA 1 (0-5s): [abertura impactante]
CENA 2 (5-15s): [mostrar produto, destacar qualidade]
CENA 3 (15-25s): [sugestão de uso/harmonização]
CENA 4 (25-30s): [call to action + preço]

LEGENDA SUGERIDA:
HASHTAGS:"""
        
        message = self.client.messages.create(
            model=settings.AI_MODEL,
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return {
            "produto": produto_nome,
            "roteiro": message.content[0].text
        }
    
    async def gerar_combo_promocional(self) -> dict:
        """Gera sugestão de combo com produtos do estoque."""
        db = SessionLocal()
        produtos = db.query(Produto).filter(Produto.estoque_atual > 0).all()
        db.close()
        
        prompt = f"""Crie um combo promocional com produtos do empório:

PRODUTOS DISPONÍVEIS:
{chr(10).join([f'- {p.nome} (R$ {p.preco_venda:.2f}) - {p.estoque_atual} unid - Margem: {p.margem_percentual}%' for p in produtos[:10]])}

Sugira:
1. Nome do combo
2. Produtos incluídos e quantidades
3. Preço original vs preço do combo
4. Desconto percentual
5. Texto para divulgação no WhatsApp"""
        
        message = self.client.messages.create(
            model=settings.AI_MODEL,
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return {"combo_sugerido": message.content[0].text}
