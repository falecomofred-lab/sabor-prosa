import anthropic
from ..config import get_settings

settings = get_settings()

class AgenteConteudo:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    
    async def gerar_post(self, tipo: str, produto_nome: str = "", produto_desc: str = "", preco: float = 0) -> dict:
        prompts = {
            "produto_dia": f"Crie um post de Instagram destacando '{produto_nome}'. Descrição: {produto_desc}. Preço: R$ {preco:.2f}. Formato: TÍTULO, TEXTO (2-3 frases tom mineiro), HASHTAGS (5), EMOJI (3).",
            "harmonizacao": f"Crie um post de harmonização para '{produto_nome}'. Formato: TÍTULO, TEXTO, HASHTAGS (5), EMOJI (3).",
            "promocao": f"Crie um post de promoção para '{produto_nome}' (R$ {preco:.2f}). Formato: TÍTULO, TEXTO, HASHTAGS (5), EMOJI (3).",
            "dica": "Crie uma dica gastronômica para empório mineiro. Formato: TÍTULO, TEXTO (2 frases), HASHTAGS (5), EMOJI (3)."
        }
        try:
            message = self.client.messages.create(model=settings.AI_MODEL, max_tokens=500, system="Você é especialista em marketing para empórios gourmet.", messages=[{"role": "user", "content": prompts.get(tipo, prompts['produto_dia'])}])
            return {"sucesso": True, "conteudo": message.content[0].text}
        except Exception as e:
            return {"sucesso": False, "erro": str(e)}
