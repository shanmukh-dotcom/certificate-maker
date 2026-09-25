import os
import uuid
import PyPDF2
from app.core.celery_app import celery_app
from app.models.database import SessionLocal
from app.models.models import GenerationJob, Event, JobStatus, Certificate, CertificateStatus, Participant, TemplateVersion, Template
from app.services.pdf_generator import generate_certificate_pdf

@celery_app.task(bind=True)
def process_generation_job(self, job_id: int):
    db = SessionLocal()
    try:
        job = db.query(GenerationJob).filter(GenerationJob.id == job_id).first()
        if not job or job.status != JobStatus.QUEUED:
            return
            
        job.status = JobStatus.PROCESSING
        db.commit()
        
        participants = db.query(Participant).filter(Participant.event_id == job.event_id).all()
        template_version = db.query(TemplateVersion).join(Template).filter(Template.organization_id == db.query(Event).filter(Event.id == job.event_id).first().organization_id).order_by(TemplateVersion.version_number.desc()).first()
        
        if not template_version:
            job.status = JobStatus.FAILED
            db.commit()
            return
            
        job.total = len(participants)
        job.pending = len(participants)
        db.commit()
        
        for p in participants:
            existing = db.query(Certificate).filter(Certificate.participant_id == p.id, Certificate.event_id == job.event_id).first()
            if existing and existing.status == CertificateStatus.ISSUED:
                if existing.pdf_path and os.path.exists(existing.pdf_path):
                    job.completed += 1
                    job.pending -= 1
                    db.commit()
                    continue
            
            try:
                cert_id_str = f"PU-CERT-{p.event_id}-{p.id}-{uuid.uuid4().hex[:6].upper()}"
                
                output_dir = f"uploads/certificates/{job.event_id}"
                os.makedirs(output_dir, exist_ok=True)
                pdf_path = os.path.join(output_dir, f"{cert_id_str}.pdf")
                
                data = p.metadata_ if p.metadata_ else {}
                data["CERTIFICATE_ID"] = cert_id_str
                data["NAME"] = p.name
                
                base_img = template_version.template.base_image_path
                generate_certificate_pdf(template_version.configuration, data, pdf_path, base_img)
                
                try:
                    with open(pdf_path, 'rb') as f:
                        reader = PyPDF2.PdfReader(f)
                        if len(reader.pages) < 1:
                            raise Exception("Empty PDF")
                except Exception as ve:
                    raise Exception(f"PDF Validation failed: {ve}")
                    
                if not existing:
                    cert = Certificate(
                        certificate_id=cert_id_str,
                        event_id=job.event_id,
                        participant_id=p.id,
                        template_version_id=template_version.id,
                        pdf_path=pdf_path,
                        status=CertificateStatus.ISSUED
                    )
                    db.add(cert)
                else:
                    existing.certificate_id = cert_id_str
                    existing.pdf_path = pdf_path
                    existing.status = CertificateStatus.ISSUED
                    
                job.completed += 1
            except Exception as e:
                job.failed += 1
                print(f"Error generating for participant {p.id}: {e}")
            
            job.pending -= 1
            db.commit()
            
        if job.failed == 0:
            job.status = JobStatus.COMPLETED
        else:
            job.status = JobStatus.PARTIAL_FAILURE
            
        db.commit()
    except Exception as e:
        print(f"Job failed completely: {e}")
    finally:
        db.close()