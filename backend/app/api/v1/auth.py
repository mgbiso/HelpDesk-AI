from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import RegisterInput, LoginInput, TokenOutput, UserOutput
from app.core.security import hash_password, verify_password, create_access_token
from app.api.v1.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/register", response_model=TokenOutput, status_code=201)
def register(data: RegisterInput, db: Session = Depends(get_db)):
    if data.role not in ("EMPLOYEE", "TECHNICIAN", "ADMIN"):
        raise HTTPException(400, "Perfil inválido")
    if db.query(User).filter(User.email == data.email.lower()).first():
        raise HTTPException(409, "Este e-mail já está cadastrado")
    user = User(name=data.name.strip(), email=data.email.lower(), password_hash=hash_password(data.password), role=data.role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"access_token": create_access_token(str(user.id)), "user": user}

@router.post("/login", response_model=TokenOutput)
def login(data: LoginInput, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email.lower()).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, "E-mail ou senha incorretos")
    return {"access_token": create_access_token(str(user.id)), "user": user}

@router.get("/me", response_model=UserOutput)
def me(user=Depends(get_current_user)):
    return user
