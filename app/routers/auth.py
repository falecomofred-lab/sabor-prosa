from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from ..auth.jwt import autenticar, criar_token

router = APIRouter(prefix="/api", tags=["Autenticacao"])

class LoginRequest(BaseModel):
    usuario: str
    senha: str

@router.post("/login")
async def login(data: LoginRequest):
    if autenticar(data.usuario, data.senha):
        token = criar_token(data.usuario)
        return JSONResponse({"token": token, "usuario": data.usuario})
    return JSONResponse({"erro": "Credenciais inválidas"}, status_code=401)
