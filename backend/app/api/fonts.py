from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.models import Font, User
from app.api.deps import get_current_user
from app.schemas.font import FontOut
import os
import shutil
import uuid

router = APIRouter(tags=["fonts"], prefix="/fonts")

UPLOAD_DIR = "uploads/fonts"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=FontOut)
async def upload_font(name: str = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    ext = file.filename.split(".")[-1].lower()
    if ext not in ["ttf", "otf", "woff"]:
        raise HTTPException(status_code=400, detail="Invalid font format")
    
    filename = f"{uuid.uuid4()}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    db_font = Font(
        organization_id=current_user.organization_id,
        name=name,
        file_path=file_path,
        format=ext
    )
    db.add(db_font)
    db.commit()
    db.refresh(db_font)
    return db_font

@router.get("/", response_model=list[FontOut])
def get_fonts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Font).filter(Font.organization_id == current_user.organization_id).all()

