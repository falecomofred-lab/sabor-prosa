from ..database import SessionLocal
from ..models import Cliente
from typing import List, Dict
from datetime import datetime

class RoteirizadorService:
    
    @staticmethod
    async def listar_entregas_pendentes() -> List[Dict]:
        """Lista clientes com entregas pendentes (simulado)."""
        db = SessionLocal()
        clientes = db.query(Cliente).filter(Cliente.endereco != "").limit(10).all()
        db.close()
        
        entregas = []
        for i, c in enumerate(clientes):
            entregas.append({
                "id": c.id,
                "cliente": c.nome,
                "endereco": c.endereco or "Endereço não cadastrado",
                "telefone": c.telefone,
                "ordem": i + 1,
                "status": "pendente",
                "horario_estimado": f"{8 + i // 3}:{str((i * 20) % 60).zfill(2)}"
            })
        
        return entregas
    
    @staticmethod
    async def otimizar_rota(entregas: List[Dict]) -> Dict:
        """Otimiza a ordem das entregas (simulação - usar Google Maps API no futuro)."""
        # Simula otimização por ordem alfabética de endereço
        otimizadas = sorted(entregas, key=lambda e: e.get("endereco", ""))
        
        for i, e in enumerate(otimizadas):
            e["ordem"] = i + 1
            e["horario_estimado"] = f"{8 + i // 3}:{str((i * 15) % 60).zfill(2)}"
        
        total_entregas = len(otimizadas)
        tempo_total = total_entregas * 15  # minutos
        
        return {
            "entregas": otimizadas,
            "total_entregas": total_entregas,
            "tempo_estimado_minutos": tempo_total,
            "tempo_estimado_horas": f"{tempo_total // 60}h{tempo_total % 60}min",
            "distancia_estimada_km": total_entregas * 3.5,
            "economia_combustivel": f"R$ {total_entregas * 2.50:.2f}",
            "horario_inicio": "08:00",
            "horario_termino": f"{8 + tempo_total // 60}:{str(tempo_total % 60).zfill(2)}",
            "dica": "Use Google Maps para otimização precisa: https://maps.google.com"
        }
    
    @staticmethod
    async def gerar_resumo_entrega() -> Dict:
        """Gera resumo diário de entregas."""
        hoje = datetime.utcnow().strftime("%d/%m/%Y")
        
        return {
            "data": hoje,
            "total_entregas": 8,
            "entregas_realizadas": 3,
            "entregas_pendentes": 5,
            "faturamento_estimado": 850.00,
            "custo_combustivel": 45.00,
            "tempo_total": "4h30min",
            "clientes_prioritarios": [
                {"nome": "João Silva", "motivo": "Cliente VIP - Entrega rápida"},
                {"nome": "Maria Souza", "motivo": "Pedido grande - R$ 250,00"}
            ]
        }
