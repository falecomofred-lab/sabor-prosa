import anthropic
from typing import Dict, Any
from ..config import get_settings

settings = get_settings()

TOOLS = [
    {
        "name": "buscar_produtos",
        "description": "Busca produtos no estoque por nome, categoria ou código de barras. Use para consultar preços, estoque e informações de produtos.",
        "input_schema": {
            "type": "object",
            "properties": {
                "busca": {"type": "string", "description": "Termo de busca (nome, categoria ou código)"}
            },
            "required": ["busca"]
        }
    },
    {
        "name": "consultar_estoque_baixo",
        "description": "Lista produtos com estoque abaixo do mínimo. Use quando perguntarem sobre reposição ou produtos acabando.",
        "input_schema": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "buscar_eventos",
        "description": "Busca eventos e feiras cadastrados. Use para informar sobre próximos eventos.",
        "input_schema": {
            "type": "object",
            "properties": {
                "busca": {"type": "string", "description": "Termo de busca"}
            },
            "required": ["busca"]
        }
    },
    {
        "name": "buscar_clientes",
        "description": "Busca clientes cadastrados por nome ou telefone.",
        "input_schema": {
            "type": "object",
            "properties": {
                "busca": {"type": "string", "description": "Nome ou telefone do cliente"}
            },
            "required": ["busca"]
        }
    },
    {
        "name": "listar_fornecedores",
        "description": "Lista fornecedores cadastrados.",
        "input_schema": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "sugerir_combo",
        "description": "Sugere um combo promocional baseado no estoque atual.",
        "input_schema": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "analisar_vendas_hoje",
        "description": "Resumo das vendas do dia (simulado).",
        "input_schema": {"type": "object", "properties": {}, "required": []}
    }
]

class ClaudeteIA:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    
    async def conversar(self, mensagem: str, db_session) -> Dict[str, Any]:
        """Conversa com Claudete, a assistente virtual do Sabor e Prosa."""
        
        SYSTEM_PROMPT = """Você é a Claudete, assistente virtual do Sabor e Prosa Empório, especializada em produtos artesanais mineiros (queijos, vinhos, cachaças, geleias, doces).

PERSONALIDADE:
- Mineira raiz, acolhedora como uma matriarca do interior
- Usa expressões mineiras com naturalidade: "uai", "trem", "sô", "bão demais", "é nóis"
- Chama todos de "meu filho" ou "minha filha"
- É prática, direta e muito conhecedora dos produtos
- Adora dar dicas de harmonização e receitas

REGRAS ABSOLUTAS:
1. NUNCA invente preços, quantidades de estoque ou dados de produtos
2. SEMPRE use as ferramentas (tools) para consultar dados reais do sistema
3. Se não encontrar a informação, seja honesta: "Ô meu filho, não achei isso aqui não. Quer que eu procure de outro jeito?"
4. Conheça TODOS os módulos do sistema: PDV, Produtos, Fornecedores, Clientes, Eventos, Kits, Rotas, Financeiro, Marketing
5. Sugira ações práticas: "Cê já deu uma olhada no Dashboard? Lá tem os alertas de estoque baixo!"

CONTEXTO DO SISTEMA:
O Sabor e Prosa Empório é um empório de produtos mineiros gerenciado pelo Thiago e pela Simone.
O sistema tem estas áreas:
- 📊 Dashboard: visão geral com métricas e alertas
- 🛒 PDV: ponto de venda com scanner de código de barras
- 📦 Produtos: cadastro de queijos, vinhos, cachaças, geleias, doces
- 👥 Clientes: CRM com histórico de compras
- 🚚 Fornecedores: cadastro com CNPJ e CEP automático
- 🎉 Eventos: agenda de feiras e festivais
- 🎁 Kits: montagem de cestas e combos
- 🗺️ Rotas: roteirizador de entregas com Google Maps
- 💰 Fechamento: fechamento de caixa com diagnóstico IA
- 📱 Marketing: gerador de posts e roteiros para redes sociais"""

        resposta = self.client.messages.create(
            model=settings.AI_MODEL,
            max_tokens=800,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": mensagem}],
            tools=TOOLS,
            tool_choice={"type": "auto"}
        )
        
        if resposta.stop_reason == "tool_use":
            resultados = []
            for bloco in resposta.content:
                if bloco.type == "tool_use":
                    result = await self._executar_ferramenta(bloco.name, bloco.input, db_session)
                    resultados.append({
                        "type": "tool_result",
                        "tool_use_id": bloco.id,
                        "content": str(result)
                    })
            
            resposta_final = self.client.messages.create(
                model=settings.AI_MODEL,
                max_tokens=800,
                system=SYSTEM_PROMPT,
                messages=[
                    {"role": "user", "content": mensagem},
                    {"role": "assistant", "content": resposta.content},
                    {"role": "user", "content": resultados}
                ]
            )
            return {"resposta": resposta_final.content[0].text, "usou_ferramentas": True}
        
        return {"resposta": resposta.content[0].text, "usou_ferramentas": False}
    
    async def _executar_ferramenta(self, nome: str, inputs: Dict, db) -> Any:
        from ..models.produto import Produto
        from ..models.evento import Evento
        from ..models.cliente import Cliente
        from ..models.fornecedor import Fornecedor
        
        if nome == "buscar_produtos":
            termo = f"%{inputs['busca']}%"
            produtos = db.query(Produto).filter(
                Produto.nome.ilike(termo) | Produto.codigo_barras.ilike(termo)
            ).limit(10).all()
            return [{"nome": p.nome, "categoria": p.categoria.value, "preco": p.preco_venda, "estoque": p.estoque_atual, "margem": p.margem_percentual} for p in produtos]
        
        elif nome == "consultar_estoque_baixo":
            produtos = db.query(Produto).filter(Produto.estoque_atual <= Produto.estoque_minimo).all()
            return [{"nome": p.nome, "estoque": p.estoque_atual, "minimo": p.estoque_minimo} for p in produtos]
        
        elif nome == "buscar_eventos":
            termo = f"%{inputs['busca']}%"
            eventos = db.query(Evento).filter(Evento.nome.ilike(termo) | Evento.local.ilike(termo)).limit(5).all()
            return [{"nome": e.nome, "data": str(e.data) if e.data else "", "local": e.local} for e in eventos]
        
        elif nome == "buscar_clientes":
            termo = f"%{inputs['busca']}%"
            clientes = db.query(Cliente).filter(Cliente.nome.ilike(termo) | Cliente.telefone.ilike(termo)).limit(5).all()
            return [{"nome": c.nome, "telefone": c.telefone, "total_compras": c.total_compras} for c in clientes]
        
        elif nome == "listar_fornecedores":
            fornecedores = db.query(Fornecedor).limit(10).all()
            return [{"nome": f.nome, "cidade": f.cidade, "uf": f.uf, "telefone": f.telefone} for f in fornecedores]
        
        elif nome == "sugerir_combo":
            produtos = db.query(Produto).filter(Produto.estoque_atual > 5).limit(5).all()
            return {"sugestao": "Combo Mineiro", "produtos": [p.nome for p in produtos]}
        
        elif nome == "analisar_vendas_hoje":
            return {"vendas": 12, "faturamento": 1850.00, "produto_mais_vendido": "Queijo Minas Artesanal"}
        
        return {}
