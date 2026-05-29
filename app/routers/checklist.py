from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from ..database import SessionLocal
from ..models import Evento, Produto
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/checklist", tags=["Checklist"])

@router.get("/feira/{evento_id}")
async def gerar_checklist(evento_id: int):
    """Gera checklist automático para uma feira/evento."""
    db = SessionLocal()
    evento = db.query(Evento).filter(Evento.id == evento_id).first()
    
    if not evento:
        db.close()
        return JSONResponse({"erro": "Evento não encontrado"}, status_code=404)
    
    dias_restantes = (evento.data - datetime.utcnow().date()).days if evento.data else 0
    
    checklist = {
        "evento": evento.nome,
        "data": evento.data.strftime("%d/%m/%Y") if evento.data else "",
        "local": evento.local,
        "dias_restantes": dias_restantes,
        "categorias": [
            {
                "categoria": "🧊 Estrutura e Conservação",
                "itens": [
                    {"item": "Caixa térmica grande (50L)", "check": False, "prioridade": "alta"},
                    {"item": "Caixa térmica média (20L)", "check": False, "prioridade": "alta"},
                    {"item": "Gelo reutilizável (mínimo 8 unidades)", "check": False, "prioridade": "alta"},
                    {"item": "Tenda/barraca 3x3", "check": False, "prioridade": "alta"},
                    {"item": "Mesa dobrável", "check": False, "prioridade": "media"},
                    {"item": "Toalha decorativa do Empório", "check": False, "prioridade": "media"},
                    {"item": "Cadeira dobrável", "check": False, "prioridade": "baixa"},
                ]
            },
            {
                "categoria": "💳 Vendas e Pagamento",
                "itens": [
                    {"item": "Maquininha de cartão CARREGADA", "check": False, "prioridade": "alta"},
                    {"item": "Celular com bateria extra (power bank)", "check": False, "prioridade": "alta"},
                    {"item": "Troco (R$ 100 em notas pequenas)", "check": False, "prioridade": "alta"},
                    {"item": "Placa de preços atualizada", "check": False, "prioridade": "media"},
                    {"item": "Bloco de notas e caneta", "check": False, "prioridade": "baixa"},
                ]
            },
            {
                "categoria": "🍽️ Degustação e Apresentação",
                "itens": [
                    {"item": "Tábua de madeira para degustação", "check": False, "prioridade": "alta"},
                    {"item": "Facas (queijo, frios, pão)", "check": False, "prioridade": "alta"},
                    {"item": "Guardanapos (mínimo 50 unidades)", "check": False, "prioridade": "media"},
                    {"item": "Palitos de dente para degustação", "check": False, "prioridade": "media"},
                    {"item": "Pratos descartáveis pequenos", "check": False, "prioridade": "media"},
                    {"item": "Embalagens para venda (sacos, caixas)", "check": False, "prioridade": "alta"},
                ]
            },
            {
                "categoria": "📋 Documentação e Marketing",
                "itens": [
                    {"item": "Cartão de visita do Empório", "check": False, "prioridade": "media"},
                    {"item": "Cardápio/Catálogo impresso", "check": False, "prioridade": "media"},
                    {"item": "Banner ou placa com nome do Empório", "check": False, "prioridade": "alta"},
                    {"item": "Comprovante de inscrição no evento", "check": False, "prioridade": "alta"},
                    {"item": "Alvará/Licença (se necessário)", "check": False, "prioridade": "alta"},
                ]
            }
        ],
        "dicas": [
            "Chegue com 1h de antecedência para montar a estrutura com calma",
            "Tire fotos da barraca montada para as redes sociais",
            "Anote o contato de outros expositores interessantes",
            "Separe um valor do caixa para comprar de outros produtores",
            "Leve água e lanche para você!"
        ]
    }
    
    db.close()
    return JSONResponse(checklist)

@router.get("/feiras-ativas")
async def feiras_com_checklist():
    """Lista eventos próximos com botão de checklist."""
    db = SessionLocal()
    hoje = datetime.utcnow().date()
    limite = hoje + timedelta(days=30)
    
    eventos = db.query(Evento).filter(
        Evento.data >= hoje,
        Evento.data <= limite
    ).order_by(Evento.data).all()
    db.close()
    
    feiras = []
    for e in eventos:
        dias = (e.data - hoje).days
        feiras.append({
            "id": e.id,
            "nome": e.nome,
            "data": e.data.strftime("%d/%m/%Y"),
            "local": e.local,
            "dias_restantes": dias,
            "urgencia": "urgente" if dias <= 3 else "atenção" if dias <= 7 else "planejar"
        })
    
    return JSONResponse({"feiras": feiras, "total": len(feiras)})
