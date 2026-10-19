from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LabRes(BaseModel):
    """实验室响应模型"""
    id: int
    name: str
    description: str | None = None
    image: str | None = None
    location: str | None = None
    capacity: int | None = 0
    open_time: str | None = None
    close_time: str | None = None
    status: int
    created: datetime | None = None
    updated: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class LabCreateRequest(BaseModel):
    """实验室创建请求模型"""
    name: str | None = None
    description: str | None = None
    image: str | None = None
    location: str | None = None
    capacity: int | None = None
    open_time: str | None = None
    close_time: str | None = None
    status: int | None = 1


class LabUpdateRequest(BaseModel):
    """实验室更新请求模型"""
    name: str | None = None
    description: str | None = None
    image: str | None = None
    location: str | None = None
    capacity: int | None = None
    open_time: str | None = None
    close_time: str | None = None
    status: int | None = None


class LabDeleteRequest(BaseModel):
    """实验室删除请求模型"""
    id: int | None = None
