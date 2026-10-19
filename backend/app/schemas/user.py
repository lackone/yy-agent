from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserRes(BaseModel):
    """用户响应模型"""
    id: int
    account: str
    username: str
    email: str | None = None
    phone: str | None = None
    avatar: str | None = None
    status: int
    is_super: int = 0
    token: str | None = None
    created: datetime | None = None
    updated: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class UserCreateRequest(BaseModel):
    """用户创建请求模型"""
    username: str | None = None
    account: str | None = None
    password: str | None = None
    email: str | None = None
    phone: str | None = None
    avatar: str | None = None
    status: int | None = 1
    is_super: int | None = 0


class UserUpdateRequest(BaseModel):
    """用户更新请求模型"""
    username: str | None = None
    password: str | None = None
    email: str | None = None
    phone: str | None = None
    avatar: str | None = None
    status: int | None = None
    is_super: int | None = None


class UserDeleteRequest(BaseModel):
    """用户删除请求模型"""
    id: int | None = None


class UserPwdChgReq(BaseModel):
    """用户密码修改请求模型"""
    old_password: str
    new_password: str
    confirm_password: str
