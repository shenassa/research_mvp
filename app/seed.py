from app.database import SessionLocal
from app.models import Department, User
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def seed_data():
    db = SessionLocal()

    try:
        # Departments
        departments = [
            "معاونت پژوهش",
            "معاونت توسعه مدیریت",
            "معاونت اجتماعی",
            "معاونت اقتصادی",
        ]

        for name in departments:
            exists = (
                db.query(Department)
                .filter(Department.name == name)
                .first()
            )

            if not exists:
                db.add(Department(name=name))

        db.commit()

        # Admin user
        admin = (
            db.query(User)
            .filter(User.username == "admin")
            .first()
        )

        if not admin:
            admin = User(
                username="admin",
                password_hash=password_hash.hash("admin123456"),
                full_name="مدیر سیستم",
                role="ADMIN",
                is_active=True
            )

            db.add(admin)
            db.commit()

        print("Initial data created successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_data()