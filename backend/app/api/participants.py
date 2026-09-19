import csv
import io
import openpyxl
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.models import Participant, Event, User
from app.api.deps import get_current_user

router = APIRouter(tags=["participants"], prefix="/participants")

@router.post("/{event_id}/upload")
async def upload_participants(event_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    event = db.query(Event).filter(Event.id == event_id, Event.organization_id == current_user.organization_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
        
    content = await file.read()
    records = []
    
    try:
        if file.filename.endswith(".csv"):
            decoded = content.decode("utf-8")
            reader = csv.DictReader(io.StringIO(decoded))
            for row in reader:
                records.append(row)
        elif file.filename.endswith(".xlsx"):
            wb = openpyxl.load_workbook(io.BytesIO(content))
            sheet = wb.active
            headers = [cell.value for cell in sheet[1]]
            for row in sheet.iter_rows(min_row=2, values_only=True):
                records.append(dict(zip(headers, row)))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error parsing file: {str(e)}")
        
    valid = 0
    errors = 0
    warnings = 0
    
    for r in records:
        name = r.get("Name", r.get("name"))
        if not name:
            errors += 1
            continue
            
        email = r.get("Email", r.get("email", ""))
        role = r.get("Role", r.get("role", ""))
        
        db_p = Participant(
            event_id=event_id,
            name=name,
            email=email,
            role=role,
            metadata_=r
        )
        db.add(db_p)
        valid += 1
        
    db.commit()
    return {"total": len(records), "valid": valid, "errors": errors, "warnings": warnings}

@router.get("/{event_id}")
def get_participants(event_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    event = db.query(Event).filter(Event.id == event_id, Event.organization_id == current_user.organization_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    participants = db.query(Participant).filter(Participant.event_id == event_id).all()
    return participants

@router.delete("/{participant_id}")
def delete_participant(participant_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    p = db.query(Participant).join(Event).filter(
        Participant.id == participant_id,
        Event.organization_id == current_user.organization_id
    ).first()
    
    if not p:
        raise HTTPException(status_code=404, detail="Participant not found")
        
    db.delete(p)
    db.commit()
    return {"message": "Deleted"}
