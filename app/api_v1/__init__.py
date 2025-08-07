from fastapi import APIRouter
from .User.routes import router as user_router
from .Account.routes import router as account_router
from .Payment.routes import router as payments_router
from .Webhoock.routes import router as webhook_router
from .Webhoock.test_webhook import router as test_webhook
router = APIRouter()
router.include_router(router=user_router)
router.include_router(router=account_router)
router.include_router(router=payments_router)
router.include_router(router=webhook_router)
router.include_router(router=test_webhook)