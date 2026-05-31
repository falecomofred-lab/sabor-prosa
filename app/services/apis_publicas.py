import httpx
from datetime import datetime, timedelta
from typing import Dict, Any, List

class APIsPublicas:
    
    # ========== CLIMA ==========
    @staticmethod
    async def previsao_tempo(cidade: str = "Niterói") -> Dict[str, Any]:
        """Previsão do tempo para planejar feiras e eventos ao ar livre."""
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"https://api.open-meteo.com/v1/forecast?latitude=-22.9068&longitude=-43.1729&daily=temperature_max,temperature_min,precipitation_probability_max,weathercode&timezone=America/Sao_Paulo&forecast_days=5", timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    daily = data.get("daily", {})
                    
                    previsao = []
                    for i in range(len(daily.get("time", []))):
                        codigo = daily["weathercode"][i]
                        clima = {0:"☀️ Limpo", 1:"🌤️ Parcial", 2:"⛅ Nublado", 3:"☁️ Encoberto", 45:"🌫️ Neblina", 61:"🌧️ Chuva", 80:"🌦️ Pancadas"}
                        
                        previsao.append({
                            "data": daily["time"][i],
                            "temp_max": daily["temperature_max"][i],
                            "temp_min": daily["temperature_min"][i],
                            "chuva_prob": daily["precipitation_probability_max"][i],
                            "clima": clima.get(codigo, "❓"),
                            "bom_para_feira": daily["precipitation_probability_max"][i] < 50
                        })
                    
                    return {"cidade": cidade, "previsao": previsao, "fonte": "Open-Meteo"}
        except:
            pass
        return {"cidade": cidade, "previsao": [], "erro": "Não foi possível obter a previsão"}
    
    # ========== FERIADOS ==========
    @staticmethod
    async def proximos_feriados() -> Dict[str, Any]:
        """Próximos feriados nacionais para planejar promoções."""
        hoje = datetime.utcnow().date()
        ano = hoje.year
        
        feriados_fixos = [
            {"data": f"{ano}-01-01", "nome": "Ano Novo", "emoji": "🎉"},
            {"data": f"{ano}-04-21", "nome": "Tiradentes", "emoji": "🇧🇷"},
            {"data": f"{ano}-05-01", "nome": "Dia do Trabalho", "emoji": "👷"},
            {"data": f"{ano}-09-07", "nome": "Independência", "emoji": "🇧🇷"},
            {"data": f"{ano}-10-12", "nome": "Nossa Senhora", "emoji": "🙏"},
            {"data": f"{ano}-11-02", "nome": "Finados", "emoji": "🕯️"},
            {"data": f"{ano}-11-15", "nome": "Proclamação", "emoji": "🇧🇷"},
            {"data": f"{ano}-12-25", "nome": "Natal", "emoji": "🎄"},
        ]
        
        proximos = []
        for f in feriados_fixos:
            data = datetime.strptime(f["data"], "%Y-%m-%d").date()
            dias = (data - hoje).days
            if 0 <= dias <= 60:
                proximos.append({**f, "dias_restantes": dias})
        
        return {
            "proximos": sorted(proximos, key=lambda x: x["dias_restantes"]),
            "dica": "Prepare kits temáticos e promoções para feriados!"
        }
    
    # ========== COTAÇÃO ==========
    @staticmethod
    async def cotacao_moedas() -> Dict[str, Any]:
        """Cotação Dólar e Euro para precificar importados."""
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get("https://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL", timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    return {
                        "dolar": {
                            "valor": float(data["USDBRL"]["bid"]),
                            "variacao": data["USDBRL"]["varBid"],
                            "data": data["USDBRL"]["create_date"]
                        },
                        "euro": {
                            "valor": float(data["EURBRL"]["bid"]),
                            "variacao": data["EURBRL"]["varBid"],
                            "data": data["EURBRL"]["create_date"]
                        },
                        "fonte": "AwesomeAPI"
                    }
        except:
            pass
        return {"erro": "Cotação indisponível"}
    
    # ========== PREÇO COMBUSTÍVEL ==========
    @staticmethod
    async def preco_gasolina() -> Dict[str, Any]:
        """Preço médio da gasolina para calcular custo de entregas."""
        return {
            "preco_medio": 5.89,
            "cidade": "Niterói",
            "data": datetime.utcnow().strftime("%d/%m/%Y"),
            "fonte": "ANP (simulado)",
            "dica": "Use o Google Maps para calcular o custo exato da rota"
        }
    
    # ========== RASTREIO CORREIOS ==========
    @staticmethod
    async def rastrear_encomenda(codigo: str) -> Dict[str, Any]:
        """Rastreia encomenda dos Correios (fornecedores)."""
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"https://proxyapp.correios.com.br/v1/sro-rastro/{codigo}", timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    eventos = data.get("objetos", [{}])[0].get("eventos", [])
                    return {
                        "codigo": codigo,
                        "status": eventos[0].get("descricao", "Não encontrado") if eventos else "Não encontrado",
                        "ultima_atualizacao": eventos[0].get("dtHrCriado", "") if eventos else "",
                        "eventos": [{"data": e.get("dtHrCriado", ""), "descricao": e.get("descricao", ""), "local": e.get("unidade", {}).get("nome", "")} for e in eventos[:5]]
                    }
        except:
            pass
        return {"codigo": codigo, "status": "Não foi possível rastrear"}
    
    # ========== RESUMO DIÁRIO ==========
    @staticmethod
    async def resumo_diario() -> Dict[str, Any]:
        """Resumo completo para o dashboard: clima + feriados + cotações."""
        clima = await APIsPublicas.previsao_tempo()
        feriados = await APIsPublicas.proximos_feriados()
        
        return {
            "clima_hoje": clima["previsao"][0] if clima.get("previsao") else None,
            "feriados_proximos": feriados.get("proximos", [])[:3],
            "mensagem": "Bom dia! ☀️" if (clima.get("previsao", [{}])[0].get("bom_para_feira", True)) else "Chuva prevista! 🌧️"
        }
