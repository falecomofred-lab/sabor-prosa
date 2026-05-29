from anthropic import Anthropic
from ..config import get_settings
from ..database import SessionLocal
from ..models import Produto, Fornecedor

settings = get_settings()

class PedidoService:
    def __init__(self):
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    
    async def gerar_pedido_inteligente(self) -> dict:
        """Gera pedido de compra baseado na Curva ABC e estoque atual."""
        db = SessionLocal()
        
        # Buscar todos os produtos
        produtos = db.query(Produto).order_by(Produto.estoque_atual.asc()).all()
        
        # Calcular Curva ABC simplificada
        produtos_ordenados = sorted(produtos, key=lambda p: p.margem_percentual, reverse=True)
        total = len(produtos_ordenados)
        
        curva_a = produtos_ordenados[:int(total * 0.2)]  # Top 20% = Classe A
        curva_b = produtos_ordenados[int(total * 0.2):int(total * 0.5)]  # 30% = Classe B
        curva_c = produtos_ordenados[int(total * 0.5):]  # 50% = Classe C
        
        # Produtos que precisam de reposição
        repor = [p for p in produtos if p.estoque_atual <= p.estoque_minimo]
        
        # Preparar dados para IA
        dados = {
            "total_produtos": total,
            "curva_a": [{"nome": p.nome, "estoque": p.estoque_atual, "minimo": p.estoque_minimo, "margem": p.margem_percentual} for p in curva_a[:5]],
            "curva_b": [{"nome": p.nome, "estoque": p.estoque_atual, "minimo": p.estoque_minimo} for p in curva_b[:5]],
            "reposicao_urgente": [{"nome": p.nome, "estoque": p.estoque_atual, "minimo": p.estoque_minimo} for p in repor[:10]]
        }
        
        db.close()
        
        # Pedir para IA gerar recomendação
        prompt = f"""Analise os dados do empório e gere um pedido de compra inteligente.

DADOS:
- Total de produtos: {dados['total_produtos']}
- Produtos Classe A (maior margem): {dados['curva_a']}
- Produtos Classe B: {dados['curva_b']}
- Precisam de reposição urgente: {dados['reposicao_urgente']}

FORMATO DA RESPOSTA:
**PEDIDO DE COMPRA - {__import__('datetime').datetime.now().strftime('%d/%m/%Y')}**

**URGENTE (estoque zerado ou abaixo do mínimo):**
- [produto]: [quantidade sugerida] unidades - motivo: [estoque atual/mínimo]

**CLASSE A (alta margem - manter estoque):**
- [produto]: [quantidade sugerida] unidades - margem atual: [X]%

**CLASSE B (média margem - revisar):**
- [produto]: [quantidade sugerida] unidades

**TOTAL ESTIMADO DO PEDIDO:** R$ [valor]"""
        
        message = self.client.messages.create(
            model=settings.AI_MODEL,
            max_tokens=800,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return {
            "sucesso": True,
            "pedido": message.content[0].text,
            "dados_crus": dados
        }
