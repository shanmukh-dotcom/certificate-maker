from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.models import GenerationJob, Event, User, JobStatus
from app.api.deps import get_current_user
from app.worker.tasks import process_generation_job

router = APIRouter(tags=["generation"], prefix="/generation")

@router.post("/{event_id}")
def start_generation(event_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    event = db.query(Event).filter(Event.id == event_id, Event.organization_id == current_user.organization_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
        
    active = db.query(GenerationJob).filter(GenerationJob.event_id == event_id, GenerationJob.status.in_([JobStatus.QUEUED, JobStatus.PROCESSING])).first()
    if active:
        raise HTTPException(status_code=400, detail="Generation already in progress.")
        
    job = GenerationJob(event_id=event_id)
    db.add(job)
    db.commit()
    db.refresh(job)
    
    process_generation_job.delay(job.id)
    return {"message": "Generation queued", "job_id": job.id}

@router.get("/{event_id}")
def get_generation_status(event_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    jobs = db.query(GenerationJob).filter(GenerationJob.event_id == event_id).order_by(GenerationJob.id.desc()).all()
    return jobs
