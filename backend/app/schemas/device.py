from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DeviceRes(BaseModel):
    """设备响应模型"""
    id: int
    lab_id: int | None = None
    lab_name: str | None = None
    name: str
    description: str | None = None
    image: str | None = None
    spec: str | None = None
    quantity: int | None = 0
    status: int
    created: datetime | None = None
    updated: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class DeviceCreateRequest(BaseModel):
    """设备创建请求模型"""
    lab_id: int | None = None
    name: str | None = None
    description: str | None = None
    image: str | None = None
    spec: str | None = None
    quantity: int | None = None
    status: int | None = 1


class DeviceUpdateRequest(BaseModel):
    """设备更新请求模型"""
    lab_id: int | None = None
    name: str | None = None
    description: str | None = None
    image: str | None = None
    spec: str | None = None
    quantity: int | None = None
    status: int | None = None


class DeviceDeleteRequest(BaseModel):
    """设备删除请求模型"""
    id: int | None = None
