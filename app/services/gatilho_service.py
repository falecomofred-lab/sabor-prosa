from datetime import datetime, timedelta
from ..database import SessionLocal
from ..models import Cliente

class GatilhoService:
    
    @staticmethod
    def verificar_reposicao():
        """Verifica clientes que compraram há mais de 20 dias e sugere contato."""
        db = SessionLocal()
        data_limite = datetime.utcnow() - timedelta(days=20)
        
        clientes = db.query(Cliente).filter(
            Cliente.ultima_compra <= data_limite,
            Cliente.ultima_compra >= datetime.utcnow() - timedelta(days=40)
        ).order_by(Cliente.ultima_compra).all()
        
        sugestoes = []
        for c in clientes:
            dias = (datetime.utcnow() - c.ultima_compra).days
            sugestoes.append({
                "cliente": c.nome,
                "telefone": c.telefone,
                "dias_sem_comprar": dias,
                "total_compras": c.total_compras,
                "mensagem": f"Olá {c.nome}! Tudo bem? Já faz {dias} dias desde sua última compra. Temos novidades fresquinhas no empório! 🧀🍷"
            })
        
        db.close()
        return sugestoes
    
    @staticmethod
    def verificar_clientes_inativos():
        """Lista clientes que não compram há mais de 30 dias."""
        db = SessionLocal()
        data_limite = datetime.utcnow() - timedelta(days=30)
        
        clientes = db.query(Cliente).filter(
            Cliente.ultima_compra <= data_limite
        ).order_by(Cliente.total_compras.desc()).limit(10).all()
        
        inativos = []
        for c in clientes:
            inativos.append({
                "cliente": c.nome,
                "telefone": c.telefone,
                "dias_inativo": (datetime.utcnow() - c.ultima_compra).days,
                "ultima_compra_valor": c.total_compras,
                "mensagem": f"Oi {c.nome}, saudades! Temos novidades no Sabor e Prosa. Vem dar uma olhada! 🎉"
            })
        
        db.close()
        return inativos
    
    @staticmethod
    def clientes_aniversariantes():
        """Verifica clientes que fazem aniversário neste mês."""
        db = SessionLocal()
        mes_atual = datetime.utcnow().month
        
        clientes = db.query(Cliente).filter(
            Cliente.data_nascimento.isnot(None)
        ).all()
        
        aniversariantes = []
        for c in clientes:
            if c.data_nascimento and c.data_nascimento.month == mes_atual:
                aniversariantes.append({
                    "cliente": c.nome,
                    "telefone": c.telefone,
                    "data_nascimento": c.data_nascimento.strftime("%d/%m"),
                    "mensagem": f"🎂 Feliz mês de aniversário, {c.nome}! Ganhe 10% off na sua próxima compra no Sabor e Prosa!"
                })
        
        db.close()
        return aniversariantes
