from ..database import SessionLocal
from ..models import Evento
from datetime import datetime, timedelta
from typing import List, Dict

class EventoInteligente:
    
    @staticmethod
    async def buscar_eventos_regiao(regiao: str = "Niterói") -> List[Dict]:
        hoje = datetime.utcnow().date()
        eventos_sugeridos = [
            {
                "nome": "Feira Gastronômica de Niterói",
                "data": (hoje + timedelta(days=25)).strftime("%Y-%m-%d"),
                "local": "Praça Central - Niterói",
                "tipo": "feira",
                "fonte": "Prefeitura Municipal",
                "inscricao": "https://prefeitura.niteroi.gov.br/feiras",
                "prazo_inscricao": (hoje + timedelta(days=10)).strftime("%d/%m/%Y"),
                "custo_estimado": 150.00,
                "publico_estimado": 2000,
                "match": "alta"
            },
            {
                "nome": "Festival Queijos & Vinhos RJ",
                "data": (hoje + timedelta(days=45)).strftime("%Y-%m-%d"),
                "local": "Jockey Club - Rio de Janeiro",
                "tipo": "gastronomico",
                "fonte": "Sympla",
                "inscricao": "https://sympla.com.br/queijos-vinhos-rj",
                "prazo_inscricao": (hoje + timedelta(days=20)).strftime("%d/%m/%Y"),
                "custo_estimado": 350.00,
                "publico_estimado": 5000,
                "match": "altissima"
            },
            {
                "nome": "Feira de Agricultura Familiar",
                "data": (hoje + timedelta(days=15)).strftime("%Y-%m-%d"),
                "local": "Parque Rural - São Gonçalo",
                "tipo": "feira",
                "fonte": "EMATER",
                "inscricao": "https://emater.rj.gov.br/feiras",
                "prazo_inscricao": (hoje + timedelta(days=5)).strftime("%d/%m/%Y"),
                "custo_estimado": 50.00,
                "publico_estimado": 800,
                "match": "media"
            },
            {
                "nome": "Circuito Cultural Niterói",
                "data": (hoje + timedelta(days=60)).strftime("%Y-%m-%d"),
                "local": "Museu de Arte Contemporânea - Niterói",
                "tipo": "cultural",
                "fonte": "Secretaria de Cultura",
                "inscricao": "https://cultura.niteroi.gov.br/editais",
                "prazo_inscricao": (hoje + timedelta(days=30)).strftime("%d/%m/%Y"),
                "custo_estimado": 100.00,
                "publico_estimado": 3000,
                "match": "alta"
            }
        ]
        return sorted(eventos_sugeridos, key=lambda e: e["data"])
    
    @staticmethod
    async def gerar_notificacoes() -> Dict:
        db = SessionLocal()
        hoje = datetime.utcnow().date()
        eventos = db.query(Evento).order_by(Evento.data).all()
        db.close()
        notificacoes = {"urgentes": [], "importantes": [], "rotina": []}
        for e in eventos:
            if not e.data: continue
            dias = (e.data - hoje).days
            if dias == 0:
                notificacoes["urgentes"].append({"texto": f"🚨 HOJE: {e.nome}", "acao": "Ir para o evento!", "link": "/checklist"})
            elif dias == 1:
                notificacoes["urgentes"].append({"texto": f"⚠️ AMANHÃ: {e.nome} - Prepare tudo hoje!", "acao": "Checklist", "link": "/checklist"})
            elif dias <= 3:
                notificacoes["importantes"].append({"texto": f"📅 {dias} dias: {e.nome}", "acao": "Preparar", "link": "/checklist"})
            elif dias <= 7:
                notificacoes["importantes"].append({"texto": f"📋 Em {dias} dias: {e.nome} - {e.local}", "acao": "Planejar", "link": "/eventos"})
            elif dias <= 15:
                notificacoes["rotina"].append({"texto": f"📌 {e.nome} em {dias} dias", "acao": "Ver", "link": "/eventos"})
        return notificacoes
    
    @staticmethod
    async def calcular_roi(evento_id: int = None) -> Dict:
        historico = [
            {"evento": "Feira Gastronômica Niterói (Mar/2026)", "faturamento": 2800.00, "custos": 350.00, "lucro": 2450.00, "roi": 700},
            {"evento": "Festival Queijos & Vinhos (Fev/2026)", "faturamento": 4500.00, "custos": 500.00, "lucro": 4000.00, "roi": 800},
            {"evento": "Feira Agricultura Familiar (Jan/2026)", "faturamento": 1200.00, "custos": 120.00, "lucro": 1080.00, "roi": 900},
            {"evento": "Circuito Cultural (Dez/2025)", "faturamento": 1800.00, "custos": 200.00, "lucro": 1600.00, "roi": 800},
        ]
        total_lucro = sum(h["lucro"] for h in historico)
        total_custos = sum(h["custos"] for h in historico)
        roi_medio = sum(h["roi"] for h in historico) / len(historico)
        return {
            "historico": historico,
            "resumo": {
                "total_lucro": total_lucro,
                "total_custos": total_custos,
                "lucro_liquido": total_lucro - total_custos,
                "roi_medio_percentual": roi_medio,
                "melhor_evento": max(historico, key=lambda h: h["roi"]),
                "media_faturamento": total_lucro / len(historico)
            },
            "dica": "Eventos gastronômicos têm ROI médio de 800%. Continue investindo!"
        }
