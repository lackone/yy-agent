from fastapi import APIRouter
from app.api.login import router as login_router
from app.api.user import router as user_router
from app.api.upload import router as upload_router
from app.api.lab import router as lab_router
from app.api.device import router as device_router
from app.api.reservation import router as reservation_router
from app.api.ai import router as ai_router

router = APIRouter(prefix="/api")

# 登录路由
router.include_router(login_router)
# 用户路由
router.include_router(user_router)
# 上传路由
router.include_router(upload_router)
# 实验室路由
router.include_router(lab_router)
# 设备路由
router.include_router(device_router)
# 预约路由
router.include_router(reservation_router)
# AI路由
router.include_router(ai_router)
