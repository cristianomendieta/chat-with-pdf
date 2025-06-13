from fastapi import APIRouter

from app.framework.apis import pdf_chat_router

router = APIRouter()
router.include_router(pdf_chat_router.api)
