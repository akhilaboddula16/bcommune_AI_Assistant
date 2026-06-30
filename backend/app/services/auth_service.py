from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.schemas.auth import SignupRequest, LoginRequest
from app.security.hashing import hash_password, verify_password
from app.security.jwt_handler import create_access_token, create_refresh_token


class AuthService:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def signup(self, data: SignupRequest):
        existing_user = self.user_repository.get_by_email(data.email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        password_hash = hash_password(data.password)

        user = self.user_repository.create_user(
            full_name=data.full_name,
            email=data.email,
            password_hash=password_hash,
        )

        self.user_repository.assign_role(
            user_id=user.id,
            role_name="User",
        )

        access_token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
            }
        )

        refresh_token = create_refresh_token(
            {
                "sub": str(user.id),
                "email": user.email,
            }
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    def login(self, data: LoginRequest):
        user = self.user_repository.get_by_email(data.email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not verify_password(data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        access_token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
            }
        )

        refresh_token = create_refresh_token(
            {
                "sub": str(user.id),
                "email": user.email,
            }
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }