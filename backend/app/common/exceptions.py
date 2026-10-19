from typing import Any

from fastapi import Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.common.response import Response


class BizException(Exception):
    """自定义业务异常"""

    def __init__(self, msg: str, code: int = 500, data: Any = {}):
        super().__init__(msg)
        self.code = code
        self.msg = msg
        self.data = data


async def biz_exception_handler(request: Request, exc: BizException):
    """自定义业务处理器"""
    return JSONResponse(
        status_code=200,
        content=Response.error(code=exc.code, msg=exc.msg, data=exc.data).model_dump(),
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """http异常处理器"""
    return JSONResponse(
        status_code=exc.status_code,
        content=Response.error(code=exc.status_code, msg=exc.detail or "未知错误", data={}).model_dump(),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """参数异常处理器"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content=Response.error(code=status.HTTP_422_UNPROCESSABLE_CONTENT, msg="请求参数校验错误",
                               data={}).model_dump(),
    )


async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理器"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=Response.error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, msg="服务器内部错误",
                               data={}).model_dump(),
    )
