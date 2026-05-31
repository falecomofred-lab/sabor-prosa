from datetime import datetime, timedelta
from jose import jwt, JWTError
from ..config import get_settings

settings = get_settings()

USUARIOS = {
    "thiago": "sabor2026",
    "simone": "prosa2026"
}

def autenticar(usuario: str, senha: str) -> bool:
    return USUARIOS.get(usuario) == senha

def criar_token(usuario: str) -> str:
    expira = datetime.utcnow() + timedelta(hours=12)
    return jwt.encode(
        {"usuario": usuario, "exp": expira},
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

def verificar_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload.get("usuario")
    except JWTError:
        return None
