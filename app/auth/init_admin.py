from sqlmodel import Session

from app.auth.crud import UserCRUD
from app.auth.models import UserCreate
from app.core.config import settings
from app.core.database import engine


def create_admin_user():
    """Create default admin user if it doesn't exist"""
    with Session(engine) as session:
        # Check if admin user already exists
        admin_user = UserCRUD.get_user_by_email(session, settings.ADMIN_EMAIL)

        if not admin_user:
            # Create admin user
            admin_user_data = UserCreate(
                email=settings.ADMIN_EMAIL,
                password=settings.ADMIN_PASSWORD,
                full_name="Admin User",
                is_active=True,
                is_superuser=True,
            )

            admin_user = UserCRUD.create_user(session, admin_user_data)
            print(f"Admin user created: {admin_user.email}")
        else:
            print(f"Admin user already exists: {admin_user.email}")


if __name__ == "__main__":
    create_admin_user()
