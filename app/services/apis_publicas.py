import httpx
from typing import Dict, Any

class APIPublicas:
    @staticmethod
    async def consultar_cnpj(cnpj: str) -> Dict[str, Any]:
        cnpj_limpo = ''.join(filter(str.isdigit, cnpj))
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_limpo}", timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    return {"razao_social": data.get("razao_social", ""), "nome_fantasia": data.get("nome_fantasia", ""), "logradouro": data.get("logradouro", ""), "bairro": data.get("bairro", ""), "cidade": data.get("municipio", ""), "uf": data.get("uf", ""), "cep": data.get("cep", ""), "telefone": data.get("ddd_telefone_1", ""), "email": data.get("email", ""), "status": "ATIVA"}
        except: pass
        return {}
    
    @staticmethod
    async def consultar_cep(cep: str) -> Dict[str, Any]:
        cep_limpo = ''.join(filter(str.isdigit, cep))
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"https://viacep.com.br/ws/{cep_limpo}/json/", timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    if "erro" not in data: return {"logradouro": data.get("logradouro", ""), "bairro": data.get("bairro", ""), "cidade": data.get("localidade", ""), "uf": data.get("uf", ""), "cep": data.get("cep", "")}
        except: pass
        return {}
    
    @staticmethod
    async def consultar_clima(cidade: str) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"https://brasilapi.com.br/api/cptec/v1/clima/previsao/{cidade.lower()}", timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    clima = data.get("clima", [])
                    if clima: return {"condicao": clima[0].get("condicao_desc", ""), "temp_min": clima[0].get("min", ""), "temp_max": clima[0].get("max", "")}
        except: pass
        return {}
