from fastapi import APIRouter, HTTPException

from app.core.security import hash_password
from app.db.postgres import SessionLocal
from app.models.database.user import UserDB
from app.schemas.auth import (
    RegisterRequest,
    RegisterResponse,
)

from fastapi import HTTPException

from app.core.security import (
    create_access_token,
    verify_password,
)
from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
)

router = APIRouter()


@router.post(
    "/register",
    response_model=RegisterResponse,
)
def register(
    request: RegisterRequest,
):
    db = SessionLocal()

    try:
        existing_user = (
            db.query(UserDB)
            .filter(
                UserDB.email == request.email
            )
            .first()
        )

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered",
            )

        user = UserDB(
            email=request.email,
            password_hash=hash_password(
                request.password
            ),
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return RegisterResponse(
            id=user.id,
            email=user.email,
        )

    finally:
        db.close()


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    request: LoginRequest,
):

    db = SessionLocal()

    try:

        user = (
            db.query(UserDB)
            .filter(
                UserDB.email == request.email
            )
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password",
            )

        if not verify_password(
            request.password,
            user.hashed_password,
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password",
            )

        token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
            }
        )

        return TokenResponse(
            access_token=token,
            token_type="bearer",
        )

    finally:
        db.close()