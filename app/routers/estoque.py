from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import JSONResponse
from ..database import SessionLocal
from ..models import Produto
import xmltodict
from datetime import datetime

router = APIRouter(prefix="/api/estoque", tags=["Estoque"])

@router.post("/importar-xml")
async def importar_xml(request: Request, arquivo: UploadFile = File(...)):
    """Importa produtos de uma NF-e (XML) e atualiza estoque."""
    try:
        conteudo = await arquivo.read()
        dados = xmltodict.parse(conteudo)
        
        # Extrair itens da NF-e
        nfe = dados.get("nfeProc", {}).get("NFe", {}).get("infNFe", {})
        itens = nfe.get("det", [])
        if not isinstance(itens, list):
            itens = [itens]
        
        db = SessionLocal()
        resultado = {"novos": [], "atualizados": [], "erros": []}
        
        for item in itens:
            try:
                prod = item.get("prod", {})
                codigo = prod.get("cProd", "")
                nome = prod.get("xProd", "")
                ean = prod.get("cEAN", "")
                quantidade = float(prod.get("qCom", 0))
                custo = float(prod.get("vUnCom", 0))
                
                # Buscar por código de barras
                existente = db.query(Produto).filter(Produto.codigo_barras == ean).first()
                
                if existente:
                    existente.estoque_atual += int(quantidade)
                    existente.preco_custo = custo
                    resultado["atualizados"].append({"nome": existente.nome, "qtd": int(quantidade)})
                else:
                    novo = Produto(
                        nome=nome,
                        categoria="Outros",
                        codigo_barras=ean,
                        preco_custo=custo,
                        preco_venda=custo * 1.5,  # Margem padrão 50%
                        estoque_atual=int(quantidade),
                        estoque_minimo=5,
                        descricao_curta=f"Importado via NF-e em {datetime.now().strftime('%d/%m/%Y')}"
                    )
                    db.add(novo)
                    resultado["novos"].append({"nome": nome, "qtd": int(quantidade)})
            except Exception as e:
                resultado["erros"].append({"item": prod.get("xProd", "Desconhecido"), "erro": str(e)})
        
        db.commit()
        db.close()
        
        return JSONResponse({"sucesso": True, "resultado": resultado})
    except Exception as e:
        return JSONResponse({"sucesso": False, "erro": str(e)}, status_code=500)
