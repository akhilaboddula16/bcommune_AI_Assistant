from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import (
    SignupRequest,
    LoginRequest,
    TokenResponse,
    CurrentUserResponse,
)
from app.services.auth_service import AuthService
from app.security.auth_dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=TokenResponse)
def signup(
    data: SignupRequest,
    db: Session = Depends(get_db),
):
    return AuthService(db).signup(data)


@router.post("/login", response_model=TokenResponse)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    return AuthService(db).login(data)


@router.get("/me", response_model=CurrentUserResponse)
def me(current_user=Depends(get_current_user)):
    return current_user