from app.models.database import User
from app.models.engine import engine
from app.modules.auth.utils import hash_password
from sqlmodel import Session


def seed_admin():
    with Session(engine) as session:
        admin = User(
            name="Admin",
            email="admin@example.com",
            password=hash_password("admin123"),
            role="admin",
        )
        session.add(admin)
        session.commit()
        print("Admin user created successfully!")


if __name__ == "__main__":
    seed_admin()
