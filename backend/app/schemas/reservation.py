from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ReservationCreateRequest(BaseModel):
    """预约创建请求模型"""
    lab_id: int
    device_id: int | None = None
    date: str
    start_time: str
    end_time: str
    remark: str | None = None


class ReservationResponse(BaseModel):
    """预约读取响应模型"""
    id: int
    user_id: int
    user_name: str | None = None
    lab_id: int
    lab_name: str | None = None
    device_id: int
    device_name: str | None = None
    type: str | None = None
    date: str
    start_time: str
    end_time: str
    remark: str | None = None
    status: int

    created: datetime | None = None
    updated: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class AuditReservationRequest(BaseModel):
    status: int  # 这里定义为 int，前端传 -1 会被正确解析为整数 -1
