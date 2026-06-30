from sqlalchemy.orm import Session

from app.models.user import User
from app.models.role import Role
from app.models.user_role import UserRole


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )

    def get_by_id(self, user_id: int) -> User | None:
        return (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    def create_user(
        self,
        full_name: str,
        email: str,
        password_hash: str,
    ) -> User:
        user = User(
            full_name=full_name,
            email=email,
            password_hash=password_hash,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def assign_role(self, user_id: int, role_name: str) -> None:
        role = (
            self.db.query(Role)
            .filter(Role.name == role_name)
            .first()
        )

        if not role:
            role = Role(name=role_name)
            self.db.add(role)
            self.db.commit()
            self.db.refresh(role)

        user_role = UserRole(
            user_id=user_id,
            role_id=role.id,
        )

        self.db.add(user_role)
        self.db.commit()