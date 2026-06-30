from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.security.auth_dependencies import get_current_user


def require_roles(allowed_roles: list[str]):
    def role_checker(
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db),
    ):
        user_roles = UserRepository(db).get_user_roles(current_user.id)

        if not any(role in allowed_roles for role in user_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
            )

        return current_user

    return role_checker