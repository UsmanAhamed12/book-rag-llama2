from fastapi import APIRouter

from app.api.routes import health as health_router
from app.api.v1.routes import auth as auth_router
from app.api.v1.routes import chat as chat_router
from app.api.v1.routes import chat_sessions as chat_sessions_router
from app.api.v1.routes import documents as documents_router
from app.api.v1.routes import upload as upload_router

api_router = APIRouter(prefix="")

api_router.include_router(health_router.router)

api_router.include_router(
    chat_router.router,
    tags=["Chat"],
)

api_router.include_router(
    chat_sessions_router.router,
)


api_router.include_router(
    upload_router.router,
    prefix="/upload",
    tags=["Upload"],
)

# api_router.include_router(
#     documents_router.api_router,
#     prefix="/documents",
#     tags=["Documents"],
# )

api_router.include_router(
    documents_router.router,
)


api_router.include_router(
    auth_router.router,
    prefix="/auth",
    tags=["Authentication"],
)
