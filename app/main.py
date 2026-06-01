from fastapi import FastAPI, Request, Form, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from .config import get_settings
from .database import engine, Base, SessionLocal
from .models import Produto, Lote, Kit, Fornecedor, Evento, Cliente, Assinante
from .routers import produtos, chatbot, dashboard, pdv, busca, kits, tags, conteudo, whatsapp, caixa, gatilhos
from .routers import produtos, chatbot, dashboard, pdv, busca, kits, tags, conteudo, whatsapp, caixa, gatilhos, roteiros
from .routers import produtos, chatbot, dashboard, pdv, busca, kits, tags, conteudo, whatsapp, caixa, gatilhos, roteiros, radar
from .routers import produtos, chatbot, dashboard, pdv, busca, kits, tags, conteudo, whatsapp, caixa, gatilhos, roteiros, radar, rotas
from .routers import produtos, chatbot, dashboard, pdv, busca, kits, tags, conteudo, whatsapp, caixa, gatilhos, roteiros, radar, rotas, monitor, checklist, vitrine_api, auth
from .auth.jwt import verificar_token
from .routers import produtos, chatbot, dashboard, pdv, busca, kits, tags, conteudo, whatsapp, caixa, gatilhos, roteiros, radar, rotas, monitor, checklist, vitrine_api, auth, qrcode
from .routers import produtos, chatbot, dashboard, pdv, busca, kits, tags, conteudo, whatsapp, caixa, gatilhos, roteiros, radar, rotas, monitor, checklist, vitrine_api, auth, qrcode, eventos_inteligentes
from .routers import produtos, chatbot, dashboard, pdv, busca, kits, tags, conteudo, whatsapp, caixa, gatilhos, roteiros, radar, rotas, monitor, checklist, vitrine_api, auth, qrcode, eventos_inteligentes, delivery
from .routers import produtos, chatbot, dashboard, pdv, busca, kits, tags, conteudo, whatsapp, caixa, gatilhos, roteiros, radar, rotas, monitor, checklist, vitrine_api, auth, qrcode, eventos_inteligentes, delivery, apis_publicas
from .routers import produtos, chatbot, dashboard, pdv, busca, kits, tags, conteudo, whatsapp, caixa, gatilhos, roteiros, radar, rotas, monitor
from .services.apis_publicas import APIsPublicas
from .services.agente_conteudo import AgenteConteudo
import os, shutil
from datetime import datetime

settings = get_settings()
Base.metadata.create_all(bind=engine)
import jinja2
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_dir))
templates = Jinja2Templates(env=env)
os.makedirs("static/fotos", exist_ok=True)
os.makedirs("static/videos", exist_ok=True)

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION, docs_url="/api/docs", redoc_url="/api/redoc")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(produtos.router)
app.include_router(chatbot.router)
app.include_router(dashboard.router)
app.include_router(pdv.router)
app.include_router(busca.router)
app.include_router(kits.router)
app.include_router(tags.router)
app.include_router(conteudo.router)
app.include_router(whatsapp.router)
app.include_router(caixa.router)
app.include_router(gatilhos.router)
app.include_router(roteiros.router)
app.include_router(radar.router)
app.include_router(rotas.router)
app.include_router(monitor.router)
app.include_router(checklist.router)
app.include_router(vitrine_api.router)
app.include_router(auth.router)
app.include_router(qrcode.router)
app.include_router(eventos_inteligentes.router)
app.include_router(delivery.router)
app.include_router(apis_publicas.router)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sabor e Prosa - Login</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: #1A120B; color: #F5E6D3; display: flex; align-items: center; justify-content: center; min-height: 100vh; }
        .login-container { text-align: center; }
        .logo { font-size: 4em; margin-bottom: 20px; }
        .card { background: #3E3526; border-radius: 16px; padding: 40px; width: 90%; max-width: 400px; margin: 0 auto; }
        .card h1 { color: #D4B896; margin-bottom: 20px; font-size: 1.5em; }
        .form-group { margin-bottom: 15px; text-align: left; }
        .form-group label { display: block; margin-bottom: 5px; color: #D4B896; }
        .form-group input { background: #2A1F14; border: 1px solid #5C4A37; color: #F5E6D3; padding: 12px; border-radius: 8px; width: 100%; font-size: 1em; }
        .btn { background: #8B6B4A; color: white; border: none; padding: 12px; border-radius: 8px; cursor: pointer; font-size: 1.1em; width: 100%; font-weight: bold; }
        .erro { color: #C23B22; margin-top: 10px; display: none; }
        .footer { margin-top: 20px; font-size: 0.85em; color: #8B6B4A; }
        .footer a { color: #D4B896; text-decoration: none; }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">🍽️</div>
        <div class="card">
            <h1>Sabor e Prosa</h1>
            <form onsubmit="return fazerLogin(event)">
                <div class="form-group">
                    <label>Usuário</label>
                    <input type="text" id="usuario" placeholder="Digite seu usuário" required>
                </div>
                <div class="form-group">
                    <label>Senha</label>
                    <input type="password" id="senha" placeholder="Digite sua senha" required>
                </div>
                <button type="submit" class="btn">🔐 Entrar</button>
                <p class="erro" id="erro">Usuário ou senha inválidos</p>
            </form>
        </div>
        <div class="footer">Desenvolvido por <a href="https://venure.com.br" target="_blank">venure.com.br</a></div>
    </div>
    <script>
        async function fazerLogin(e) {
            e.preventDefault();
            const usuario = document.getElementById('usuario').value;
            const senha = document.getElementById('senha').value;
            const resp = await fetch('/api/login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({usuario, senha})
            });
            if (resp.ok) {
                const data = await resp.json();
                localStorage.setItem('token', data.token);
                localStorage.setItem('usuario', data.usuario);
                window.location.href = '/dashboard';
            } else {
                document.getElementById('erro').style.display = 'block';
            }
        }
    </script>
</body>
</html>"""
    return HTMLResponse(content=html)

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    # Redirecionar para home
    return RedirectResponse(url="/")

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    db = SessionLocal()
    pl = db.query(Produto).all()
    m = round(sum(p.margem_percentual for p in pl)/len(pl),1) if pl else 0
    db.close()
    return templates.TemplateResponse("dashboard.html", {"request":request,"total_produtos":len(pl),"total_estoque":sum(p.estoque_atual for p in pl),"margem_media":m,"alertas":len([p for p in pl if p.estoque_atual <= p.estoque_minimo])})

@app.get("/produtos", response_class=HTMLResponse)
async def listar_produtos_html(request: Request):
    db = SessionLocal(); pl = db.query(Produto).order_by(Produto.nome).all(); db.close()
    return templates.TemplateResponse("produtos.html", {"request":request,"produtos":pl,"editando":None})

@app.get("/produtos/editar/{pid}", response_class=HTMLResponse)
async def editar_produto_html(request: Request, pid: int):
    db = SessionLocal(); p = db.query(Produto).filter(Produto.id==pid).first(); pl = db.query(Produto).order_by(Produto.nome).all(); db.close()
    return templates.TemplateResponse("produtos.html", {"request":request,"produtos":pl,"editando":p})

@app.post("/api/produtos/form")
async def criar_produto_form(nome:str=Form(...),categoria:str=Form(...),codigo_barras:str=Form(""),preco_custo:float=Form(...),preco_venda:float=Form(...),estoque_atual:int=Form(0),estoque_minimo:int=Form(5),validade:str=Form(""),descricao_curta:str=Form(""),historia:str=Form(""),foto:UploadFile=File(None),id:int=Form(None)):
    db = SessionLocal(); fu=""
    if foto and foto.filename:
        ext=foto.filename.split(".")[-1]; fn=f"prod_{id or 'n'}_{abs(hash(foto.filename))}.{ext}"
        with open(f"static/fotos/{fn}","wb") as b: shutil.copyfileobj(foto.file,b)
        fu=f"/static/fotos/{fn}"
    if id:
        p=db.query(Produto).filter(Produto.id==id).first()
        for a in['nome','categoria','codigo_barras','preco_custo','preco_venda','estoque_atual','estoque_minimo','descricao_curta','historia']: setattr(p,a,locals()[a])
        p.validade=validade if validade else None
        if fu: p.foto_url=fu
    else:
        db.add(Produto(nome=nome,categoria=categoria,codigo_barras=codigo_barras,preco_custo=preco_custo,preco_venda=preco_venda,estoque_atual=estoque_atual,estoque_minimo=estoque_minimo,validade=validade if validade else None,descricao_curta=descricao_curta,historia=historia,foto_url=fu))
    db.commit(); db.close()
    return RedirectResponse(url="/produtos",status_code=303)

@app.get("/fornecedores", response_class=HTMLResponse)
async def fornecedores_html(request: Request):
    db = SessionLocal(); fl = db.query(Fornecedor).order_by(Fornecedor.nome).all(); db.close()
    return templates.TemplateResponse("fornecedores.html", {"request":request,"fornecedores":fl,"editando":None})

@app.get("/fornecedores/editar/{fid}", response_class=HTMLResponse)
async def editar_fornecedor_html(request: Request, fid: int):
    db = SessionLocal(); f = db.query(Fornecedor).filter(Fornecedor.id==fid).first(); fl = db.query(Fornecedor).order_by(Fornecedor.nome).all(); db.close()
    return templates.TemplateResponse("fornecedores.html", {"request":request,"fornecedores":fl,"editando":f})

@app.post("/api/fornecedores/form")
async def criar_fornecedor_form(id:int=Form(None),nome:str=Form(...),cnpj:str=Form(""),contato:str=Form(""),telefone:str=Form(""),email:str=Form(""),cep:str=Form(""),logradouro:str=Form(""),bairro:str=Form(""),cidade:str=Form(""),uf:str=Form(""),observacoes:str=Form("")):
    db = SessionLocal()
    if id:
        f=db.query(Fornecedor).filter(Fornecedor.id==id).first()
        for a in['nome','cnpj','contato','telefone','email','cep','logradouro','bairro','cidade','uf','observacoes']: setattr(f,a,locals()[a])
    else: db.add(Fornecedor(nome=nome,cnpj=cnpj,contato=contato,telefone=telefone,email=email,cep=cep,logradouro=logradouro,bairro=bairro,cidade=cidade,uf=uf,observacoes=observacoes))
    db.commit(); db.close()
    return RedirectResponse(url="/fornecedores",status_code=303)

@app.get("/clientes", response_class=HTMLResponse)
async def clientes_html(request: Request):
    db = SessionLocal(); cl = db.query(Cliente).order_by(Cliente.nome).all(); db.close()
    return templates.TemplateResponse("clientes.html", {"request":request,"clientes":cl})

@app.post("/api/clientes/form")
async def criar_cliente_form(nome:str=Form(...),telefone:str=Form(...),email:str=Form(""),cpf:str=Form(""),data_nascimento:str=Form(""),endereco:str=Form(""),observacoes:str=Form("")):
    db = SessionLocal()
    dn = datetime.strptime(data_nascimento,"%Y-%m-%d").date() if data_nascimento else None
    db.add(Cliente(nome=nome,telefone=telefone,email=email,cpf=cpf,data_nascimento=dn,endereco=endereco,observacoes=observacoes))
    db.commit(); db.close()
    return RedirectResponse(url="/clientes",status_code=303)

@app.get("/eventos", response_class=HTMLResponse)
async def eventos_html(request: Request):
    db = SessionLocal(); el = db.query(Evento).order_by(Evento.data).all(); db.close()
    return templates.TemplateResponse("eventos.html", {"request":request,"eventos":el})

@app.post("/api/eventos/form")
async def criar_evento_form(nome:str=Form(...),data:str=Form(""),local:str=Form(""),tipo:str=Form(""),descricao:str=Form("")):
    db = SessionLocal()
    d = datetime.strptime(data,"%Y-%m-%d").date() if data else None
    db.add(Evento(nome=nome,data=d,local=local,tipo=tipo,descricao=descricao))
    db.commit(); db.close()
    return RedirectResponse(url="/eventos",status_code=303)

@app.get("/conteudo", response_class=HTMLResponse)
async def conteudo_html(request: Request):
    db = SessionLocal(); pl = db.query(Produto).order_by(Produto.nome).all(); db.close()
    return templates.TemplateResponse("conteudo.html", {"request":request,"produtos":pl})

@app.get("/pdv", response_class=HTMLResponse)
async def pdv_html(request: Request): return templates.TemplateResponse("pdv.html", {"request":request})

@app.get("/kits", response_class=HTMLResponse)
async def kits_html(request: Request):
    db = SessionLocal(); kl = db.query(Kit).order_by(Kit.nome).all(); pl = db.query(Produto).order_by(Produto.nome).all(); db.close()
    return templates.TemplateResponse("kits.html", {"request":request,"kits":kl,"produtos":pl,"editando":None})

@app.get("/kits/editar/{kid}", response_class=HTMLResponse)
async def editar_kit_html(request: Request, kid: int):
    db = SessionLocal(); k = db.query(Kit).filter(Kit.id==kid).first(); kl = db.query(Kit).order_by(Kit.nome).all(); pl = db.query(Produto).order_by(Produto.nome).all(); db.close()
    return templates.TemplateResponse("kits.html", {"request":request,"kits":kl,"produtos":pl,"editando":k})

@app.get("/busca", response_class=HTMLResponse)
async def busca_html(request: Request): return templates.TemplateResponse("busca.html", {"request":request})

@app.get("/tela-cliente", response_class=HTMLResponse)
async def tela_cliente(request: Request): return templates.TemplateResponse("tela_cliente.html", {"request":request})

@app.get("/api/consultas/cnpj")
async def consulta_cnpj(cnpj: str = Query(...)): return JSONResponse(await APIsPublicas.consultar_cnpj(cnpj))

@app.get("/api/consultas/cep")
async def consulta_cep(cep: str = Query(...)): return JSONResponse(await APIsPublicas.consultar_cep(cep))

@app.get("/api/consultas/clima")
async def consulta_clima(cidade: str = Query(...)): return JSONResponse(await APIsPublicas.consultar_clima(cidade))

@app.get("/api/pdv/carrinho-ativo")
async def carrinho_ativo(): return JSONResponse({"itens": [], "total": 0})

@app.get("/vitrine", response_class=HTMLResponse)
async def vitrine_publica(request: Request):
    return templates.TemplateResponse("vitrine.html", {"request": request})

@app.get("/gatilhos", response_class=HTMLResponse)
async def gatilhos_html(request: Request):
    return templates.TemplateResponse("gatilhos.html", {"request": request})

@app.get("/estudio", response_class=HTMLResponse)
async def estudio_html(request: Request):
    db = SessionLocal(); pl = db.query(Produto).order_by(Produto.nome).all(); db.close()
    return templates.TemplateResponse("estudio.html", {"request": request, "produtos": pl})

@app.get("/radar", response_class=HTMLResponse)
async def radar_html(request: Request):
    return templates.TemplateResponse("radar.html", {"request": request})

@app.get("/rotas", response_class=HTMLResponse)
async def rotas_html(request: Request):
    return templates.TemplateResponse("rotas.html", {"request": request})

@app.get("/monitor", response_class=HTMLResponse)
async def monitor_html(request: Request):
    return templates.TemplateResponse("monitor.html", {"request": request})

@app.get("/checklist", response_class=HTMLResponse)
async def checklist_html(request: Request):
    return templates.TemplateResponse("checklist.html", {"request": request})

@app.get("/tutorial", response_class=HTMLResponse)
async def tutorial_html(request: Request):
    return templates.TemplateResponse("tutorial.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/cadastro-evento", response_class=HTMLResponse)
async def cadastro_evento_page(request: Request):
    return templates.TemplateResponse("cadastro-evento.html", {"request": request})

@app.post("/api/clientes/cadastro-evento")
async def cadastro_evento_api(data: dict):
    db = SessionLocal()
    nome = data.get("nome", "")
    telefone = data.get("telefone", "")
    origem = data.get("origem", "feira")
    evento = data.get("evento", "QR Code")
    db.add(Cliente(nome=nome, telefone=telefone, observacoes=f"Origem: {origem} | Evento: {evento}"))
    db.commit()
    db.close()
    return JSONResponse({"sucesso": True})

@app.get("/qrcode", response_class=HTMLResponse)
async def qrcode_page(request: Request):
    return templates.TemplateResponse("qrcode.html", {"request": request})

@app.get("/api/eventos/listar")
async def listar_eventos_api():
    db = SessionLocal()
    eventos = db.query(Evento).order_by(Evento.data).all()
    resultado = []
    for e in eventos:
        resultado.append({
            "id": e.id,
            "nome": e.nome,
            "data": str(e.data) if e.data else "",
            "local": e.local,
            "tipo": e.tipo,
            "descricao": e.descricao
        })
    db.close()
    return JSONResponse(resultado)

@app.get("/api/kits/listar")
async def listar_kits_api():
    db = SessionLocal()
    kits_list = db.query(Kit).order_by(Kit.nome).all()
    resultado = []
    for k in kits_list:
        itens = []
        for item in k.itens:
            itens.append({
                "id": item.id,
                "nome": item.nome,
                "preco_custo": item.preco_custo,
                "quantidade": 1
            })
        resultado.append({
            "id": k.id,
            "nome": k.nome,
            "descricao": k.descricao,
            "preco_venda": k.preco_venda,
            "margem_percentual": k.margem_percentual,
            "itens": itens
        })
    db.close()
    return JSONResponse(resultado)

@app.get("/static/manifest.json")
async def manifest():
    return FileResponse("app/static/manifest.json", media_type="application/json")

@app.get("/api/fornecedores")
async def listar_fornecedores_api():
    db = SessionLocal()
    fornecedores = db.query(Fornecedor).order_by(Fornecedor.nome).all()
    resultado = []
    for f in fornecedores:
        resultado.append({
            "id": f.id,
            "nome": f.nome,
            "cnpj": f.cnpj,
            "contato": f.contato,
            "telefone": f.telefone,
            "email": f.email,
            "cep": f.cep,
            "logradouro": f.logradouro,
            "bairro": f.bairro,
            "cidade": f.cidade,
            "uf": f.uf,
            "observacoes": f.observacoes
        })
    db.close()
    return JSONResponse(resultado)

@app.get("/api/clientes/listar")
async def listar_clientes_api():
    db = SessionLocal()
    clientes = db.query(Cliente).order_by(Cliente.nome).all()
    resultado = []
    for c in clientes:
        resultado.append({
            "id": c.id,
            "nome": c.nome,
            "telefone": c.telefone,
            "email": c.email,
            "cpf": c.cpf,
            "data_nascimento": str(c.data_nascimento) if c.data_nascimento else "",
            "endereco": c.endereco,
            "total_compras": c.total_compras,
            "ultima_compra": str(c.ultima_compra) if c.ultima_compra else "",
            "observacoes": c.observacoes
        })
    db.close()
    return JSONResponse(resultado)

@app.get("/health")
async def health_check(): return {"status":"healthy"}

@app.get("/auditoria", response_class=HTMLResponse)
async def auditoria_html(request: Request):
    return templates.TemplateResponse("auditoria.html", {"request": request})

@app.get("/fechamento", response_class=HTMLResponse)
async def fechamento_html(request: Request):
    return templates.TemplateResponse("fechamento.html", {"request": request})
