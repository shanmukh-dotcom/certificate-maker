from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.models import Event, User
from app.api.deps import get_current_user
from app.schemas.event import EventCreate, EventUpdate, EventOut

router = APIRouter(tags=["events"], prefix="/events")

@router.get("/", response_model=list[EventOut])
def read_events(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    events = db.query(Event).filter(Event.organization_id == current_user.organization_id).all()
    return events

@router.post("/", response_model=EventOut)
def create_event(event: EventCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_event = Event(**event.model_dump(), organization_id=current_user.organization_id)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.get("/{event_id}", response_model=EventOut)
def read_event(event_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    event = db.query(Event).filter(Event.id == event_id, Event.organization_id == current_user.organization_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

