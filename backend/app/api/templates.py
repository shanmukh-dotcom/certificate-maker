from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.models import Template, TemplateVersion, User
from app.api.deps import get_current_user
from app.schemas.template import TemplateCreate, TemplateOut, TemplateVersionCreate, TemplateVersionOut
import os
import shutil
import uuid

router = APIRouter(tags=["templates"], prefix="/templates")

UPLOAD_DIR = "uploads/templates"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=TemplateOut)
async def create_template(name: str = Form(...), file: UploadFile = File(None), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    file_path = None
    if file:
        ext = file.filename.split(".")[-1].lower()
        if ext not in ["png", "jpg", "jpeg", "pdf"]:
            raise HTTPException(status_code=400, detail="Invalid background image format")
        filename = f"{uuid.uuid4()}.{ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
    db_template = Template(
        organization_id=current_user.organization_id,
        name=name,
        base_image_path=file_path
    )
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template

@router.get("/", response_model=list[TemplateOut])
def get_templates(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Template).filter(Template.organization_id == current_user.organization_id).all()

@router.post("/{template_id}/versions", response_model=TemplateVersionOut)
def create_template_version(template_id: int, version_in: TemplateVersionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    template = db.query(Template).filter(Template.id == template_id, Template.organization_id == current_user.organization_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
        
    # Get highest version
    latest = db.query(TemplateVersion).filter(TemplateVersion.template_id == template_id).order_by(TemplateVersion.version_number.desc()).first()
    next_version = (latest.version_number + 1) if latest else 1
    
    db_version = TemplateVersion(
        template_id=template_id,
        version_number=next_version,
        configuration=version_in.configuration
    )
    db.add(db_version)
    db.commit()
    db.refresh(db_version)
    return db_version

@router.get("/{template_id}/versions", response_model=list[TemplateVersionOut])
def get_template_versions(template_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(TemplateVersion).filter(TemplateVersion.template_id == template_id).all()



from app.services.pdf_generator import generate_certificate_pdf
from fastapi.responses import FileResponse

@router.post("/{template_id}/versions/{version_id}/test")
def test_generate_certificate(template_id: int, version_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    template = db.query(Template).filter(Template.id == template_id, Template.organization_id == current_user.organization_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    version = db.query(TemplateVersion).filter(TemplateVersion.id == version_id, TemplateVersion.template_id == template_id).first()
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")
    
    sample_data = {
        "NAME": "Alexander Rajesh Kumar",
        "EVENT_NAME": "Advanced Artificial Intelligence Workshop",
        "CERTIFICATE_ID": "PU-AI-2026-001247"
    }
    
    output_file = os.path.join("/tmp", f"test_{version_id}.pdf")
    # On Windows, /tmp might be issue. Use a local temp directory.
    temp_dir = "local_temp"
    os.makedirs(temp_dir, exist_ok=True)
    output_file = os.path.join(temp_dir, f"test_{version.id}.pdf")

    generate_certificate_pdf(version.configuration, sample_data, output_file, template.base_image_path)

    return FileResponse(output_file, media_type="application/pdf", filename="test_certificate.pdf")
