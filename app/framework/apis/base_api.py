from fastapi import APIRouter

from app.framework.apis import assistant_router

router = APIRouter()
router.include_router(assistant_router.api)
