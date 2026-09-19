from app.models.database import SessionLocal
from app.models.models import User, Organization, UserRole
from app.core.security import get_password_hash

db = SessionLocal()

org = db.query(Organization).first()
if not org:
    org = Organization(name="Default Organization")
    db.add(org)
    db.commit()
    db.refresh(org)

admin = db.query(User).filter(User.email == "admin@example.com").first()
if not admin:
    admin = User(
        organization_id=org.id,
        name="Admin",
        email="admin@example.com",
        password_hash=get_password_hash("admin123"),
        role=UserRole.ADMIN
    )
    db.add(admin)
    db.commit()
    print("Admin user created: admin@example.com / admin123")
else:
    print("Admin already exists.")
