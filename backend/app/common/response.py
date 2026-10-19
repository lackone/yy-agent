from typing import Any

from pydantic import BaseModel


class Response(BaseModel):
    """响应模型"""

    code: int
    msg: str
    data: Any = None

    @classmethod
    def success(cls, msg: str = '成功', data: Any = {}):
        """成功响应"""
        return cls(code=200, msg=msg, data=data)

    @classmethod
    def error(cls, code: int = 500, msg: str = '失败', data: Any = {}):
        """失败响应"""
        return cls(code=code, msg=msg, data=data)


class PageResponse(BaseModel):
    """分页响应模型"""
    total: int
    list: Any = []
