from ..database import SessionLocal
from ..models import Evento
from datetime import datetime, timedelta
from typing import List, Dict

class RadarEventos:
    
    @staticmethod
    async def buscar_eventos_proximos() -> Dict:
        """Busca eventos cadastrados nos próximos 60 dias."""
        db = SessionLocal()
        hoje = datetime.utcnow().date()
        limite = hoje + timedelta(days=60)
        
        eventos = db.query(Evento).filter(
            Evento.data >= hoje,
            Evento.data <= limite
        ).order_by(Evento.data).all()
        db.close()
        
        proximos = []
        urgente = []
        
        for e in eventos:
            dias = (e.data - hoje).days
            evento_dict = {
                "nome": e.nome,
                "data": e.data.strftime("%d/%m/%Y") if e.data else "",
                "local": e.local,
                "tipo": e.tipo,
                "dias_restantes": dias,
                "status": "inscricoes_abertas" if dias > 7 else "urgente"
            }
            if dias <= 7:
                urgente.append(evento_dict)
            else:
                proximos.append(evento_dict)
        
        return {
            "urgentes": urgente,
            "proximos": proximos,
            "total": len(eventos),
            "mensagem": f"{len(urgente)} eventos urgentes e {len(proximos)} nos próximos 60 dias"
        }
    
    @staticmethod
    async def sugerir_eventos_externos(regiao: str = "Minas Gerais") -> Dict:
        """Sugere tipos de eventos para buscar na região."""
        sugestoes = [
            {
                "tipo": "Feira Gastronômica",
                "onde_buscar": "Sympla, Eventbrite, Instagram",
                "periodo": "Mensal",
                "acao": "Buscar 'feira gastronômica {regiao}' no Google"
            },
            {
                "tipo": "Feira de Queijos e Vinhos",
                "onde_buscar": "Secretaria de Turismo, SEBRAE",
                "periodo": "Trimestral",
                "acao": "Cadastrar no SEBRAE para receber alertas"
            },
            {
                "tipo": "Feira de Agricultura Familiar",
                "onde_buscar": "EMATER, Prefeitura",
                "periodo": "Mensal",
                "acao": "Contatar EMATER local"
            },
            {
                "tipo": "Festival Gastronômico",
                "onde_buscar": "Google Events, Facebook Events",
                "periodo": "Bimestral",
                "acao": "Seguir páginas de turismo da região"
            },
            {
                "tipo": "Feira Livre / Orgânicos",
                "onde_buscar": "Prefeitura Municipal",
                "periodo": "Semanal",
                "acao": "Consultar calendário oficial da cidade"
            }
        ]
        
        return {
            "regiao": regiao,
            "sugestoes": sugestoes,
            "dica": "Configure o Google Alerta para: 'feira gastronômica OR festival gastronômico OR feira de queijos {regiao}'"
        }
    
    @staticmethod
    async def verificar_oportunidades() -> Dict:
        """Verifica eventos próximos e gera alertas de ação."""
        db = SessionLocal()
        hoje = datetime.utcnow().date()
        limite = hoje + timedelta(days=30)
        
        eventos = db.query(Evento).filter(
            Evento.data >= hoje,
            Evento.data <= limite
        ).order_by(Evento.data).all()
        db.close()
        
        alertas = []
        for e in eventos:
            dias = (e.data - hoje).days
            if dias <= 3:
                alertas.append(f"🚨 ÚLTIMA CHANCE: {e.nome} em {dias} dias ({e.data.strftime('%d/%m')}) - {e.local}")
            elif dias <= 7:
                alertas.append(f"⚠️ ATENÇÃO: {e.nome} em {dias} dias - prepare estoque e materiais")
            elif dias <= 15:
                alertas.append(f"📅 AGENDAR: {e.nome} em {dias} dias - verificar inscrições")
            else:
                alertas.append(f"📋 PLANEJAR: {e.nome} em {dias} dias - {e.local}")
        
        return {
            "total_oportunidades": len(alertas),
            "alertas": alertas,
            "timestamp": datetime.utcnow().strftime("%d/%m/%Y %H:%M")
        }
