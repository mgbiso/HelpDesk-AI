from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.models.ticket import Ticket
from app.api.v1.dependencies import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary")
def summary(db: Session = Depends(get_db), user=Depends(get_current_user)):
    query = db.query(Ticket)
    if user.role == "EMPLOYEE":
        query = query.filter(Ticket.requester_id == user.id)
    total = query.count()
    statuses = {row[0]: row[1] for row in query.with_entities(Ticket.status, func.count(Ticket.id)).group_by(Ticket.status).all()}
    priorities = {row[0]: row[1] for row in query.with_entities(Ticket.priority, func.count(Ticket.id)).group_by(Ticket.priority).all()}
    return {"total": total, "open": statuses.get("OPEN", 0), "in_progress": statuses.get("IN_PROGRESS", 0),
            "resolved": statuses.get("RESOLVED", 0) + statuses.get("CLOSED", 0), "by_status": statuses, "by_priority": priorities}
