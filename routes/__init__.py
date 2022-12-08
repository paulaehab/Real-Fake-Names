from fastapi import APIRouter
from .api import userRoutes

routes = APIRouter()

routes.include_router(userRoutes)