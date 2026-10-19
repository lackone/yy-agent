import os
import traceback

from app.services import kb_service

# 设置 HuggingFace 国内镜像，必须在 import chromadb 之前执行！
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
# os.environ["HTTP_PROXY"] = "http://127.0.0.1:7897"
# os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7897"

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from app.common.exceptions import BizException, biz_exception_handler, http_exception_handler, \
    validation_exception_handler, global_exception_handler
from app.config.config import UPLOADS_DIR
from app.core.database import BaseModel, engine
from app.api.api import router as api_router
from app.services.reservation_service import run_expire_reservation


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理器"""
    print("startup ")

    try:
        await asyncio.to_thread(kb_service.warmup)
    except Exception:
        traceback.print_exc()

    # 启动预约过期任务
    task = asyncio.create_task(run_expire_reservation())

    yield
    print("shutdown ")

    # 取消预约过期任务
    task.cancel()


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# 允许所有来源访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# 注册路由
app.include_router(api_router)

# 注册异常处理器
app.add_exception_handler(BizException, biz_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

# 挂载静态文件目录
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")


# 初始化数据库
def init_db():
    from app.models.user import User
    from app.models.lab import Lab
    from app.models.device import Device
    from app.models.reservation import Reservation

    # 自动帮我们创建数据库和数据库表
    BaseModel.metadata.create_all(engine)


init_db()


@app.get("/")
def read_root():
    return {"message": "Hello World"}
