import os
from app.models.database import SessionLocal
from app.models.models import User, UserRole

db = SessionLocal()
user = db.query(User).filter(User.email == 'admin@certify.com').first()
if user:
    user.role = UserRole.ADMIN
    db.commit()
print('User role fixed')