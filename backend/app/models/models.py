from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base
import enum

class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    ORGANIZER = "ORGANIZER"

class EventStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    READY = "READY" 
    GENERATING = "GENERATING"
    ISSUED = "ISSUED"
    ARCHIVED = "ARCHIVED"


class CertificateStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    GENERATING = "GENERATING"
    VALIDATED = "VALIDATED"
    ISSUED = "ISSUED"
    REVOKED = "REVOKED"
    FAILED = "FAILED"


class JobStatus(str, enum.Enum):
    QUEUED = "QUEUED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    PARTIAL_FAILURE = "PARTIAL_FAILURE"
    FAILED = "FAILED"


class Organization(Base):
    __tablename__ = "organizations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    users = relationship("User", back_populates="organization")
    events = relationship("Event", back_populates="organization")
    fonts = relationship("Font", back_populates="organization")
    templates = relationship("Template", back_populates="organization")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    organization = relationship("Organization", back_populates="users")

class Font(Base):
    __tablename__ = "fonts"
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    name = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    format = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    organization = relationship("Organization", back_populates="fonts")

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    issue_date = Column(DateTime, nullable=True)
    status = Column(Enum(EventStatus), default=EventStatus.DRAFT)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    organization = relationship("Organization", back_populates="events")
    participants = relationship("Participant", back_populates="event")

class Template(Base):
    __tablename__ = "templates"
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    name = Column(String(255), nullable=False)
    base_image_path = Column(String(512), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    organization = relationship("Organization", back_populates="templates")
    versions = relationship("TemplateVersion", back_populates="template")

class TemplateVersion(Base):
    __tablename__ = "template_versions"
    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey("templates.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    configuration = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    template = relationship("Template", back_populates="versions")

class Participant(Base):
    __tablename__ = "participants"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    role = Column(String(255), nullable=True)
    metadata_ = Column("metadata", JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    event = relationship("Event", back_populates="participants")

class Certificate(Base):
    __tablename__ = "certificates"
    id = Column(Integer, primary_key=True, index=True)
    certificate_id = Column(String(100), unique=True, index=True, nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    participant_id = Column(Integer, ForeignKey("participants.id"), nullable=False)
    template_version_id = Column(Integer, ForeignKey("template_versions.id"), nullable=False)
    pdf_path = Column(String(512), nullable=True)
    status = Column(Enum(CertificateStatus), default=CertificateStatus.DRAFT)
    issued_at = Column(DateTime, nullable=True)
    revoked_at = Column(DateTime, nullable=True)
    revocation_reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class GenerationJob(Base):
    __tablename__ = "generation_jobs"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    total = Column(Integer, default=0)
    completed = Column(Integer, default=0)
    failed = Column(Integer, default=0)
    pending = Column(Integer, default=0)
    status = Column(Enum(JobStatus), default=JobStatus.QUEUED)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class GenerationError(Base):
    __tablename__ = "generation_errors"
    id = Column(Integer, primary_key=True, index=True)
    generation_job_id = Column(Integer, ForeignKey("generation_jobs.id"), nullable=False)
    participant_id = Column(Integer, ForeignKey("participants.id"), nullable=True)
    certificate_id = Column(String(100), nullable=True)
    error_code = Column(String(100), nullable=False)
    error_message = Column(Text, nullable=False)
    retry_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(255), nullable=False)
    entity_type = Column(String(255), nullable=False)
    entity_id = Column(String(255), nullable=True)
    metadata_ = Column("metadata", JSON, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

