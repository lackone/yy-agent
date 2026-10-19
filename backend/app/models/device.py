from sqlalchemy import Integer, ForeignKey, String, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import BaseModel
from app.models.lab import Lab


class Device(BaseModel):
    __tablename__ = "devices"
    __table_args__ = (
        Index("idx_lab_id", "lab_id"),
        {"comment": "设备表"}
    )

    lab_id: Mapped[int] = mapped_column(Integer, server_default="0", comment="实验室ID", nullable=False)
    name: Mapped[str] = mapped_column(String(32), server_default="", comment="设备名称", nullable=False)
    description: Mapped[str] = mapped_column(String(500), server_default="", comment="设备描述", nullable=False)
    image: Mapped[str] = mapped_column(String(256), server_default="", comment="设备图片", nullable=False)
    spec: Mapped[str] = mapped_column(String(500), server_default="", comment="设备规格", nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, server_default="0", comment="设备数量", nullable=False)
    status: Mapped[int] = mapped_column(Integer, server_default="1", comment="设备状态, 1: 正常, -1: 禁用",
                                        nullable=False)

    lab: Mapped[Lab] = relationship(primaryjoin="Device.lab_id == Lab.id", foreign_keys="Device.lab_id",
                                    lazy="selectin", )
