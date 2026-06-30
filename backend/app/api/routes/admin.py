from fastapi import APIRouter, Depends

from app.security.rbac import require_roles

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/dashboard")
def admin_dashboard(
    current_user=Depends(require_roles(["Super Admin", "Admin"])),
):
    return {
        "message": "Welcome to Admin Dashboard",
        "user": current_user.email,
    }


@router.get("/super-admin")
def super_admin_only(
    current_user=Depends(require_roles(["Super Admin"])),
):
    return {
        "message": "Welcome Super Admin",
        "user": current_user.email,
    }