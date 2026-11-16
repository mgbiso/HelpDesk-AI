from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.session import get_db
from app.models.ticket import Ticket, Comment, TicketHistory
from app.schemas.ticket import TicketCreate, TicketUpdate, TicketOutput, CommentCreate, CommentOutput
from app.api.v1.dependencies import get_current_user, require_staff

router = APIRouter(prefix="/tickets", tags=["Chamados"])
STATUSES = {"OPEN", "IN_PROGRESS", "WAITING", "RESOLVED", "CLOSED"}
PRIORITIES = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}

def classify(text: str):
    value = text.lower()
    rules = [
        (("senha", "login", "acesso", "bloqueado"), "Acesso", "MEDIUM"),
        (("internet", "rede", "wifi", "wi-fi", "conexão"), "Rede", "HIGH"),
        (("computador", "notebook", "tela", "teclado", "mouse"), "Hardware", "MEDIUM"),
        (("sistema", "erro", "aplicativo", "software", "programa"), "Software", "HIGH"),
        (("urgente", "parado", "todos", "empresa inteira"), "Incidente crítico", "CRITICAL"),
    ]
    for words, category, priority in rules:
        if any(word in value for word in words):
            return category, priority, "Classificação automática baseada em palavras-chave. Revise antes de agir."
    return "Geral", "MEDIUM", "Não foi possível identificar uma categoria específica; triagem manual recomendada."

@router.get("", response_model=list[TicketOutput])
def list_tickets(db: Session = Depends(get_db), user=Depends(get_current_user)):
    query = db.query(Ticket)
    if user.role == "EMPLOYEE":
        query = query.filter(Ticket.requester_id == user.id)
    return query.order_by(desc(Ticket.created_at)).all()

@router.post("", response_model=TicketOutput, status_code=201)
def create_ticket(data: TicketCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    category, suggested_priority, _ = classify(data.title + " " + data.description)
    priority = data.priority if data.priority in PRIORITIES else suggested_priority
    ticket = Ticket(title=data.title, description=data.description, category=data.category if data.category != "Geral" else category,
                    priority=priority, requester_id=user.id)
    db.add(ticket)
    db.flush()
    db.add(TicketHistory(ticket_id=ticket.id, user_id=user.id, action="CREATED", details="Chamado aberto"))
    db.commit()
    db.refresh(ticket)
    return ticket

@router.get("/{ticket_id}", response_model=TicketOutput)
def get_ticket(ticket_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    ticket = db.get(Ticket, ticket_id)
    if not ticket or (user.role == "EMPLOYEE" and ticket.requester_id != user.id):
        raise HTTPException(404, "Chamado não encontrado")
    return ticket

@router.patch("/{ticket_id}", response_model=TicketOutput)
def update_ticket(ticket_id: int, data: TicketUpdate, db: Session = Depends(get_db), user=Depends(require_staff)):
    ticket = db.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(404, "Chamado não encontrado")
    changes = data.model_dump(exclude_unset=True)
    if "status" in changes and changes["status"] not in STATUSES:
        raise HTTPException(400, "Status inválido")
    if "priority" in changes and changes["priority"] not in PRIORITIES:
        raise HTTPException(400, "Prioridade inválida")
    for key, value in changes.items():
        setattr(ticket, key, value)
    db.add(TicketHistory(ticket_id=ticket.id, user_id=user.id, action="UPDATED", details=str(changes)))
    db.commit()
    db.refresh(ticket)
    return ticket

@router.get("/{ticket_id}/comments", response_model=list[CommentOutput])
def list_comments(ticket_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    ticket = db.get(Ticket, ticket_id)
    if not ticket or (user.role == "EMPLOYEE" and ticket.requester_id != user.id):
        raise HTTPException(404, "Chamado não encontrado")
    return db.query(Comment).filter(Comment.ticket_id == ticket_id).order_by(Comment.created_at).all()

@router.post("/{ticket_id}/comments", response_model=CommentOutput, status_code=201)
def add_comment(ticket_id: int, data: CommentCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    ticket = db.get(Ticket, ticket_id)
    if not ticket or (user.role == "EMPLOYEE" and ticket.requester_id != user.id):
        raise HTTPException(404, "Chamado não encontrado")
    comment = Comment(ticket_id=ticket_id, user_id=user.id, content=data.content)
    db.add(comment)
    db.add(TicketHistory(ticket_id=ticket_id, user_id=user.id, action="COMMENTED", details="Comentário adicionado"))
    db.commit()
    db.refresh(comment)
    return comment

@router.get("/meta/ai-classify")
def ai_classify(text: str, user=Depends(get_current_user)):
    category, priority, explanation = classify(text)
    return {"category": category, "suggested_priority": priority, "explanation": explanation}
