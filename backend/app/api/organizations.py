from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.models import Organization, User
from app.api.deps import get_current_user, get_current_admin
from app.schemas.organization import OrganizationCreate, OrganizationOut

router = APIRouter(tags=["organizations"], prefix="/organizations")

@router.get("/", response_model=list[OrganizationOut])
def read_organizations(db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    orgs = db.query(Organization).all()
    return orgs

@router.post("/", response_model=OrganizationOut)
def create_organization(org: OrganizationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    db_org = Organization(**org.model_dump())
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    return db_org

