from fastapi import APIRouter

from src.messenger import urls as messenger_routes
from src.viber import ulrs as viber_routes

api_router = APIRouter()
api_router.include_router(messenger_routes.router, tags=["messenger-app"])
api_router.include_router(viber_routes.router, tags=["viber-app"])
