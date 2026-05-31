import httpx
from typing import Dict, Any
from datetime import datetime

class DeliveryService:
    
    @staticmethod
    async def cotar_entrega(
        origem_cep: str,
        destino_cep: str,
        peso_kg: float = 2.0
    ) -> Dict[str, Any]:
        """Simula cotação de frete com serviços de moto delivery."""
        
        # Simulação de cotações (no futuro, integrar com APIs reais)
        cotacoes = [
            {
                "servico": "99Entregas",
                "prazo": "30-45 min",
                "valor": round(8.50 + (peso_kg * 1.5), 2),
                "tipo": "Moto",
                "icone": "🏍️",
                "link": "https://99app.com/entregas"
            },
            {
                "servico": "Loggi",
                "prazo": "40-60 min",
                "valor": round(10.00 + (peso_kg * 1.2), 2),
                "tipo": "Moto",
                "icone": "🛵",
                "link": "https://www.loggi.com"
            },
            {
                "servico": "MotoLink",
                "prazo": "25-40 min",
                "valor": round(7.00 + (peso_kg * 1.8), 2),
                "tipo": "Moto",
                "icone": "🏍️",
                "link": "https://motolink.com.br"
            }
        ]
        
        return {
            "origem": origem_cep,
            "destino": destino_cep,
            "peso": peso_kg,
            "cotacoes": sorted(cotacoes, key=lambda x: x["valor"]),
            "data": datetime.utcnow().strftime("%d/%m/%Y %H:%M")
        }
    
    @staticmethod
    async def solicitar_entrega(
        servico: str,
        origem: str,
        destino: str,
        contato_origem: str,
        contato_destino: str,
        descricao: str = "Alimentos perecíveis - Embalagem térmica"
    ) -> Dict[str, Any]:
        """Simula solicitação de entrega (no futuro, API real)."""
        
        return {
            "sucesso": True,
            "servico": servico,
            "codigo_rastreio": f"SP-{datetime.utcnow().strftime('%Y%m%d%H%M')}",
            "previsao_retirada": "15-20 minutos",
            "previsao_entrega": "45-60 minutos",
            "status": "Aguardando motoboy",
            "link_rastreio": "https://99app.com/entregas/rastrear",
            "mensagem": f"🚀 {servico} acionado! Motoboy a caminho para retirada."
        }
