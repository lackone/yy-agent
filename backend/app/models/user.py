from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import BaseModel


class User(BaseModel):
    """用户模型"""
    __tablename__ = "users"
    __table_args__ = {"comment": "用户表"}

    account: Mapped[str] = mapped_column(String(32), server_default="", comment="账号", nullable=False)
    password: Mapped[str] = mapped_column(String(255), server_default="", comment="密码", nullable=False)
    username: Mapped[str] = mapped_column(String(32), server_default="", comment="用户名称", nullable=False)
    email: Mapped[str | None] = mapped_column(String(64), server_default="", comment="邮箱", nullable=False)
    phone: Mapped[str | None] = mapped_column(String(16), server_default="", comment="手机号", nullable=False)
    avatar: Mapped[str | None] = mapped_column(String(255), server_default="", comment="头像", nullable=False)
    status: Mapped[int] = mapped_column(default=1, server_default="1", comment="-1禁用，1启用", nullable=False)
    is_super: Mapped[int] = mapped_column(default=0, server_default="0", comment="是否超级管理员", nullable=False)
