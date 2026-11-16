from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import auth, tickets, dashboard

app = FastAPI(title="HelpDesk AI", description="Plataforma inteligente de gerenciamento de chamados de TI", version="1.0.0")

origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(auth.router, prefix="/api/v1")
app.include_router(tickets.router, prefix="/api/v1")
app.include_router(dashboard.router, prefix="/api/v1")

@app.get("/")
def home():
    return {"message": "HelpDesk AI API", "docs": "/docs", "status": "online"}

@app.get("/health")
def health():
    return {"status": "healthy"}
