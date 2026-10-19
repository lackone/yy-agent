from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import BaseModel


class Lab(BaseModel):
    """实验室模型"""
    __tablename__ = "labs"
    __table_args__ = {"comment": "实验室表"}

    name: Mapped[str] = mapped_column(String(32), server_default="", comment="实验室名称", nullable=False)
    description: Mapped[str] = mapped_column(String(500), server_default="", comment="实验室描述", nullable=False)
    image: Mapped[str] = mapped_column(String(256), server_default="", comment="实验室图片", nullable=False)
    location: Mapped[str] = mapped_column(String(32), server_default="", comment="实验室位置", nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, server_default="0", comment="实验室容量", nullable=False)
    open_time: Mapped[str] = mapped_column(String(32), server_default="", comment="实验室开放时间", nullable=False)
    close_time: Mapped[str] = mapped_column(String(32), server_default="", comment="实验室关闭时间", nullable=False)
    status: Mapped[int] = mapped_column(Integer, server_default="1", comment="实验室状态, 1: 正常, -1: 禁用",
                                        nullable=False)
