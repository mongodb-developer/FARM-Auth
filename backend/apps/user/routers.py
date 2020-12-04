from fastapi import APIRouter, Request
from config import settings

from .models import UserDB
from .auth import jwt_authentication


def get_users_router(app):
    users_router = APIRouter()

    def on_after_register(user: UserDB, request: Request):
        print(f"User {user.id} has registered.")

    def on_after_forgot_password(user: UserDB, token: str, request: Request):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    users_router.include_router(
        app.fastapi_users.get_auth_router(jwt_authentication),
        prefix="/auth/jwt",
        tags=["auth"],
    )
    users_router.include_router(
        app.fastapi_users.get_register_router(on_after_register),
        prefix="/auth",
        tags=["auth"],
    )
    users_router.include_router(
        app.fastapi_users.get_reset_password_router(
            settings.JWT_SECRET_KEY, after_forgot_password=on_after_forgot_password
        ),
        prefix="/auth",
        tags=["auth"],
    )
    users_router.include_router(
        app.fastapi_users.get_users_router(), prefix="/users", tags=["users"]
    )

    return users_router
