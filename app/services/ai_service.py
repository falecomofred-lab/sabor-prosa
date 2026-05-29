import anthropic
from typing import Dict, Any
from ..config import get_settings

settings = get_settings()

TOOLS = [
    {"name": "buscar_produtos", "description": "Busca produtos no banco por nome, categoria ou código. Use SEMPRE antes de responder sobre produtos.", "input_schema": {"type": "object", "properties": {"busca": {"type": "string"}}, "required": ["busca"]}},
    {"name": "buscar_eventos", "description": "Busca eventos cadastrados.", "input_schema": {"type": "object", "properties": {"busca": {"type": "string"}}, "required": ["busca"]}},
    {"name": "consultar_estoque_baixo", "description": "Lista produtos com estoque abaixo do mínimo.", "input_schema": {"type": "object", "properties": {}, "required": []}}
]

class AIService:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    
    async def chat_with_tools(self, user_message: str, db_session) -> Dict[str, Any]:
        SYSTEM_PROMPT = "Você é a Prosa, assistente do Sabor e Prosa Empório. REGRAS: 1) NUNCA invente preços ou estoque. 2) SEMPRE use buscar_produtos antes de falar de produtos. 3) Tom mineiro acolhedor."
        response = self.client.messages.create(model=settings.AI_MODEL, max_tokens=1024, system=SYSTEM_PROMPT, messages=[{"role": "user", "content": user_message}], tools=TOOLS, tool_choice={"type": "auto"})
        if response.stop_reason == "tool_use":
            tool_results = []
            for content in response.content:
                if content.type == "tool_use":
                    result = await self._execute_tool(content.name, content.input, db_session)
                    tool_results.append({"type": "tool_result", "tool_use_id": content.id, "content": str(result)})
            final_response = self.client.messages.create(model=settings.AI_MODEL, max_tokens=1024, system=SYSTEM_PROMPT, messages=[{"role": "user", "content": user_message}, {"role": "assistant", "content": response.content}, {"role": "user", "content": tool_results}])
            return {"texto": final_response.content[0].text, "usou_tools": True}
        return {"texto": response.content[0].text, "usou_tools": False}
    
    async def _execute_tool(self, tool_name: str, inputs: Dict, db) -> Any:
        from ..models.produto import Produto
        from ..models.evento import Evento
        if tool_name == "buscar_produtos":
            produtos = db.query(Produto).filter(Produto.nome.ilike(f"%{inputs['busca']}%")).limit(10).all()
            return [{"nome": p.nome, "preco": p.preco_venda, "estoque": p.estoque_atual} for p in produtos]
        elif tool_name == "buscar_eventos":
            eventos = db.query(Evento).filter(Evento.nome.ilike(f"%{inputs['busca']}%")).limit(10).all()
            return [{"nome": e.nome, "data": str(e.data), "local": e.local} for e in eventos]
        elif tool_name == "consultar_estoque_baixo":
            produtos = db.query(Produto).filter(Produto.estoque_atual <= Produto.estoque_minimo).all()
            return [{"nome": p.nome, "estoque": p.estoque_atual} for p in produtos]
