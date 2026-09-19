import os
import zipfile
import tempfile
import time
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.models import Certificate, Participant, Event, CertificateStatus, User, AuditLog
from app.api.deps import get_current_user
from fastapi.responses import FileResponse
from pydantic import BaseModel

router = APIRouter(tags=["certificates"], prefix="/certificates")


@router.get("/")
def get_certificates(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    certs = db.query(Certificate).join(Event).filter(
        Event.organization_id == current_user.organization_id
    ).order_by(Certificate.issued_at.desc()).limit(100).all()

    result = []
    for c in certs:
        participant = db.query(Participant).filter(Participant.id == c.participant_id).first()
        event = db.query(Event).filter(Event.id == c.event_id).first()
        result.append({
            "certificate_id": c.certificate_id,
            "participant_name": participant.name if participant else "Unknown",
            "event_name": event.name if event else "Unknown",
            "issued_at": c.issued_at,
            "status": c.status.value,
            "pdf_url": c.pdf_path
        })
    return result


class RevokeRequest(BaseModel):
    reason: str


@router.get("/verify/{certificate_id}")
def verify_certificate(certificate_id: str, db: Session = Depends(get_db)):
    cert = db.query(Certificate).filter(Certificate.certificate_id == certificate_id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="CERTIFICATE NOT FOUND")

    if cert.status == CertificateStatus.REVOKED:
        raise HTTPException(status_code=400, detail="CERTIFICATE REVOKED")

    if cert.status != CertificateStatus.ISSUED:
        raise HTTPException(status_code=400, detail="Certificate is not issued")

    participant = db.query(Participant).filter(Participant.id == cert.participant_id).first()
    event = db.query(Event).filter(Event.id == cert.event_id).first()

    return {
        "certificate_id": cert.certificate_id,
        "name": participant.name if participant else "Unknown",
        "event_name": event.name if event else "Unknown",
        "issued_on": cert.issued_at,
        "status": "VALID"
    }


@router.post("/{certificate_id}/revoke")
def revoke_certificate(certificate_id: str, req: RevokeRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cert = db.query(Certificate).join(Event).filter(
        Certificate.certificate_id == certificate_id,
        Event.organization_id == current_user.organization_id
    ).first()

    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")

    cert.status = CertificateStatus.REVOKED
    cert.revocation_reason = req.reason

    audit = AuditLog(
        user_id=current_user.id,
        action="CERTIFICATE_REVOKED",
        entity_type="certificate",
        entity_id=certificate_id,
        metadata_={"reason": req.reason}
    )
    db.add(audit)
    db.commit()

    return {"message": "Certificate revoked successfully"}


@router.get("/{certificate_id}/download")
def download_certificate(certificate_id: str, db: Session = Depends(get_db)):
    cert = db.query(Certificate).filter(Certificate.certificate_id == certificate_id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Not found")

    if not cert.pdf_path or not os.path.exists(cert.pdf_path):
        raise HTTPException(status_code=404, detail="File not found on disk")

    return FileResponse(cert.pdf_path, media_type="application/pdf", filename=f"{certificate_id}.pdf")


@router.get("/events/{event_id}/download-zip")
def download_event_zip(event_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    event = db.query(Event).filter(Event.id == event_id, Event.organization_id == current_user.organization_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    certs = db.query(Certificate).filter(Certificate.event_id == event_id, Certificate.status == CertificateStatus.ISSUED).all()
    if not certs:
        raise HTTPException(status_code=400, detail="No issued certificates found for this event")

    temp_dir = os.path.join(tempfile.gettempdir(), f"certify_exports_{int(time.time())}")
    os.makedirs(temp_dir, exist_ok=True)
    zip_path = os.path.join(temp_dir, f"certificates_event_{event_id}.zip")

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for cert in certs:
            if cert.pdf_path and os.path.exists(cert.pdf_path):
                participant = db.query(Participant).filter(Participant.id == cert.participant_id).first()
                safe_name = "".join([c for c in participant.name if c.isalpha() or c.isdigit() or c == ' ']).rstrip()
                filename = f"{safe_name}_{cert.certificate_id}.pdf"
                zipf.write(cert.pdf_path, filename)

    return FileResponse(zip_path, media_type="application/zip", filename=f"certificates_event_{event_id}.zip")