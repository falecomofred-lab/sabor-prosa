import httpx
from typing import Dict, Any, List
from datetime import datetime

class DeliveryService:
    
    @staticmethod
    async def cotar_entrega(
        origem_cep: str,
        destino_cep: str,
        peso_kg: float = 2.0
    ) -> Dict[str, Any]:
        """Simula cotação de frete com serviços de moto delivery."""
        
        cotacoes = [
            {
                "servico": "Delivery Niterói",
                "prazo": "25-40 min",
                "valor": round(9.90 + (peso_kg * 1.8), 2),
                "tipo": "Moto",
                "icone": "🏍️",
                "regiao": "Niterói e São Gonçalo",
                "site": "https://deliveryniteroi.com.br",
                "link": "https://deliveryniteroi.com.br/solicitar"
            },
            {
                "servico": "MotoFlash RJ",
                "prazo": "30-45 min",
                "valor": round(11.50 + (peso_kg * 1.5), 2),
                "tipo": "Moto",
                "icone": "🛵",
                "regiao": "Niterói, São Gonçalo e Rio",
                "site": "https://motoflashrj.com.br",
                "link": "https://motoflashrj.com.br/entrega"
            },
            {
                "servico": "99Entregas",
                "prazo": "30-45 min",
                "valor": round(8.50 + (peso_kg * 1.5), 2),
                "tipo": "Moto",
                "icone": "🏍️",
                "regiao": "Nacional",
                "site": "https://99app.com/entregas",
                "link": "https://99app.com/entregas"
            },
            {
                "servico": "Loggi",
                "prazo": "40-60 min",
                "valor": round(10.00 + (peso_kg * 1.2), 2),
                "tipo": "Moto",
                "icone": "🛵",
                "regiao": "Nacional",
                "site": "https://www.loggi.com",
                "link": "https://www.loggi.com/cotar"
            },
            {
                "servico": "Rapiddo (Rede Local)",
                "prazo": "20-35 min",
                "valor": round(7.50 + (peso_kg * 2.0), 2),
                "tipo": "Moto",
                "icone": "🏍️",
                "regiao": "Niterói e Grande Rio",
                "site": "https://rapiddo.com.br",
                "link": "https://rapiddo.com.br/solicitar"
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
            "mensagem": f"🚀 {servico} acionado! Motoboy a caminho para retirada."
        }