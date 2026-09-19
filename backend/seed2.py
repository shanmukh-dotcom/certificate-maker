import os
from app.models.database import SessionLocal
from app.models.models import User, Organization
from app.core.security import get_password_hash

db = SessionLocal()
org = db.query(Organization).filter(Organization.name == 'CERTIFY Org').first()
if not org:
    org = Organization(name='CERTIFY Org')
    db.add(org)
    db.commit()
    db.refresh(org)

user = db.query(User).filter(User.email == 'admin@certify.com').first()
if not user:
    user = User(name='Admin', email='admin@certify.com', password_hash=get_password_hash('securepassword123'), organization_id=org.id, role='admin')
    db.add(user)
    db.commit()
print('User created')