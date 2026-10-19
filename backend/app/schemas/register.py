from pydantic import BaseModel, ConfigDict


class RegisterReq(BaseModel):
    """注册请求模型"""
    account: str
    password: str
    repassword: str


class RegisterRes(BaseModel):
    """注册响应模型"""
    id: int
    account: str
    username: str
    email: str | None = None
    phone: str | None = None
    avatar: str | None = None
    status: int

    model_config = ConfigDict(from_attributes=True)
