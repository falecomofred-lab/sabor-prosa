from typing import List, Dict
from datetime import datetime

class MonitorPrecos:
    
    @staticmethod
    async def listar_produtos_monitorados() -> List[Dict]:
        """Lista de insumos que o Thiago precisa comprar regularmente."""
        return [
            {
                "categoria": "Embalagens",
                "itens": [
                    {"nome": "Caixa de Papelão P", "preco_medio": 2.50, "unidade": "unidade", "fornecedor": "Embalagens Express"},
                    {"nome": "Caixa de Papelão M", "preco_medio": 3.80, "unidade": "unidade", "fornecedor": "Embalagens Express"},
                    {"nome": "Caixa de Papelão G", "preco_medio": 5.20, "unidade": "unidade", "fornecedor": "Embalagens Express"},
                    {"nome": "Saco Kraft Personalizado", "preco_medio": 1.80, "unidade": "unidade", "fornecedor": "Grafica Print"},
                    {"nome": "Etiqueta Adesiva", "preco_medio": 0.35, "unidade": "unidade", "fornecedor": "Grafica Print"},
                ]
            },
            {
                "categoria": "Caixas Térmicas",
                "itens": [
                    {"nome": "Caixa Térmica 10L", "preco_medio": 45.00, "unidade": "unidade", "fornecedor": "TermoBox"},
                    {"nome": "Caixa Térmica 20L", "preco_medio": 75.00, "unidade": "unidade", "fornecedor": "TermoBox"},
                    {"nome": "Caixa Térmica 50L", "preco_medio": 120.00, "unidade": "unidade", "fornecedor": "TermoBox"},
                    {"nome": "Gelo Reutilizável", "preco_medio": 12.00, "unidade": "unidade", "fornecedor": "TermoBox"},
                ]
            },
            {
                "categoria": "Frete e Transporte",
                "itens": [
                    {"nome": "Frete MG-SP (10kg)", "preco_medio": 35.00, "unidade": "por envio", "fornecedor": "Transportadora Rápida"},
                    {"nome": "Frete MG-SP (20kg)", "preco_medio": 55.00, "unidade": "por envio", "fornecedor": "Transportadora Rápida"},
                    {"nome": "Frete MG-RJ (10kg)", "preco_medio": 45.00, "unidade": "por envio", "fornecedor": "Transportadora Rápida"},
                ]
            },
            {
                "categoria": "Material de Feira",
                "itens": [
                    {"nome": "Tenda 3x3", "preco_medio": 350.00, "unidade": "unidade", "fornecedor": "Feira Mix"},
                    {"nome": "Mesa Dobrável", "preco_medio": 120.00, "unidade": "unidade", "fornecedor": "Feira Mix"},
                    {"nome": "Toalha Decorativa", "preco_medio": 45.00, "unidade": "unidade", "fornecedor": "Feira Mix"},
                    {"nome": "Placa de Preço", "preco_medio": 15.00, "unidade": "kit 10un", "fornecedor": "Feira Mix"},
                ]
            }
        ]
    
    @staticmethod
    async def verificar_alertas_precos() -> Dict:
        """Simula verificação de promoções e gera alertas."""
        hoje = datetime.utcnow().strftime("%d/%m/%Y")
        
        return {
            "data": hoje,
            "alertas": [
                {
                    "tipo": "promocao",
                    "prioridade": "alta",
                    "produto": "Caixa Térmica 20L",
                    "preco_normal": 75.00,
                    "preco_promocional": 59.90,
                    "desconto": "20%",
                    "fornecedor": "TermoBox",
                    "link": "https://www.termobox.com.br/promocao",
                    "validade": "Oferta válida até amanhã!"
                },
                {
                    "tipo": "promocao",
                    "prioridade": "media",
                    "produto": "Saco Kraft Personalizado (lote 500un)",
                    "preco_normal": 1.80,
                    "preco_promocional": 1.35,
                    "desconto": "25%",
                    "fornecedor": "Grafica Print",
                    "link": "https://www.graficaprint.com.br",
                    "validade": "Válido por 3 dias"
                },
                {
                    "tipo": "promocao",
                    "prioridade": "alta",
                    "produto": "Frete MG-SP (10kg)",
                    "preco_normal": 35.00,
                    "preco_promocional": 28.00,
                    "desconto": "20%",
                    "fornecedor": "Transportadora Rápida",
                    "link": "https://www.transportadorarapida.com.br",
                    "validade": "Último dia!"
                },
                {
                    "tipo": "alerta",
                    "prioridade": "baixa",
                    "produto": "Tenda 3x3",
                    "preco_normal": 350.00,
                    "preco_promocional": 299.00,
                    "desconto": "15%",
                    "fornecedor": "Feira Mix",
                    "link": "https://www.feiramix.com.br",
                    "validade": "Promoção do mês"
                }
            ],
            "economia_total": 108.10,
            "dicas": [
                "Compre em quantidade para ganhar desconto progressivo",
                "Compare preços em pelo menos 3 fornecedores",
                "Cadastre-se nas newsletters para receber ofertas",
                "Negocie frete grátis em compras acima de R$ 200"
            ],
            "onde_buscar": [
                {"site": "Google Shopping", "url": "https://shopping.google.com"},
                {"site": "Mercado Livre", "url": "https://www.mercadolivre.com.br"},
                {"site": "Amazon", "url": "https://www.amazon.com.br"},
                {"site": "Shopee", "url": "https://shopee.com.br"},
            ]
        }
    
    @staticmethod
    async def sugerir_fornecedores_alternativos() -> Dict:
        """Sugere fornecedores alternativos para pesquisa."""
        return {
            "categorias": [
                {
                    "categoria": "Embalagens",
                    "fornecedores": [
                        {"nome": "Embalagens Express", "site": "embalagensexpress.com.br", "diferencial": "Frete grátis acima de R$ 100"},
                        {"nome": "Caixa & Cia", "site": "caixacia.com.br", "diferencial": "Desconto no primeiro pedido"},
                        {"nome": "Pack Store", "site": "packstore.com.br", "diferencial": "Personalização inclusa"},
                    ]
                },
                {
                    "categoria": "Caixas Térmicas",
                    "fornecedores": [
                        {"nome": "TermoBox", "site": "termobox.com.br", "diferencial": "Maior variedade"},
                        {"nome": "IsoporNet", "site": "isopornet.com.br", "diferencial": "Preço mais baixo"},
                        {"nome": "CoolerPro", "site": "coolerpro.com.br", "diferencial": "Maior durabilidade"},
                    ]
                }
            ],
            "dica_negociacao": "Sempre peça desconto para compra em quantidade e combine fretes!"
        }
