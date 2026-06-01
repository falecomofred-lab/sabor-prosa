from ..database import SessionLocal
from ..models import Evento
from datetime import datetime, timedelta
from typing import List, Dict

class EventoInteligente:
    
    @staticmethod
    async def buscar_eventos_regiao(regiao: str = "Niterói") -> List[Dict]:
        """Retorna links e dicas reais para buscar eventos na região."""
        hoje = datetime.utcnow().date()
        
        return [
            {
                "nome": "🔗 Sympla - Buscar eventos em " + regiao,
                "data": "",
                "local": "Online",
                "tipo": "link",
                "fonte": "Sympla",
                "inscricao": f"https://www.sympla.com.br/eventos?q={regiao}&tipo=feira+gastronomica",
                "prazo_inscricao": "Buscar agora",
                "custo_estimado": 0,
                "publico_estimado": 0,
                "match": "alta",
                "acao": "Buscar no Sympla"
            },
            {
                "nome": "🔗 Eventbrite - Eventos em " + regiao,
                "data": "",
                "local": "Online",
                "tipo": "link",
                "fonte": "Eventbrite",
                "inscricao": f"https://www.eventbrite.com.br/d/brazil--{regiao}/food-and-drink/",
                "prazo_inscricao": "Buscar agora",
                "custo_estimado": 0,
                "publico_estimado": 0,
                "match": "alta",
                "acao": "Buscar no Eventbrite"
            },
            {
                "nome": "🔗 Prefeitura de " + regiao + " - Editais e Feiras",
                "data": "",
                "local": regiao,
                "tipo": "link",
                "fonte": "Prefeitura Municipal",
                "inscricao": f"https://www.google.com/search?q=prefeitura+{regiao}+editais+feiras+gastronomicas",
                "prazo_inscricao": "Buscar agora",
                "custo_estimado": 0,
                "publico_estimado": 0,
                "match": "alta",
                "acao": "Buscar Editais"
            },
            {
                "nome": "🔗 SEBRAE - Capacitação e Feiras",
                "data": "",
                "local": "Regional",
                "tipo": "link",
                "fonte": "SEBRAE",
                "inscricao": "https://www.sebrae.com.br/sites/PortalSebrae/ufs/rj",
                "prazo_inscricao": "Buscar agora",
                "custo_estimado": 0,
                "publico_estimado": 0,
                "match": "media",
                "acao": "Acessar SEBRAE RJ"
            },
            {
                "nome": "🔗 Google Alertas - Monitorar oportunidades",
                "data": "",
                "local": "Online",
                "tipo": "link",
                "fonte": "Google Alertas",
                "inscricao": f"https://www.google.com/alerts?q=feira+gastronomica+{regiao}",
                "prazo_inscricao": "Configurar agora",
                "custo_estimado": 0,
                "publico_estimado": 0,
                "match": "media",
                "acao": "Criar Alerta"
            }
        ]
    
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