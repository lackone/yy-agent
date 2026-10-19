from pydantic import BaseModel, ConfigDict


class LoginReq(BaseModel):
    """登录请求模型"""
    account: str
    password: str


class LoginRes(BaseModel):
    """登录响应模型"""
    id: int
    account: str
    username: str
    email: str | None = None
    phone: str | None = None
    avatar: str | None = None
    status: int
    token: str | None = None

    model_config = ConfigDict(from_attributes=True)
