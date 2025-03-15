from aiogram import Router

from .sites import router as sites_router

main_router = Router()

main_router.include_router(sites_router)

__all__ = ("main_router",)
