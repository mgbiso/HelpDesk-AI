
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import decode_token
from app.models.user import User

bearer_scheme = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    payload = decode_token(token)

    if not payload or not payload.get("sub"):
        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado"
        )

    user = db.get(User, int(payload["sub"]))

    if not user or not user.is_active:
        raise HTTPException(
            status_code=401,
            detail="Usuário não encontrado ou inativo"
        )

    return user


def require_staff(user=Depends(get_current_user)):
    if user.role not in ("ADMIN", "TECHNICIAN"):
        raise HTTPException(
            status_code=403,
            detail="Acesso permitido apenas à equipe de suporte"
        )

    return user
