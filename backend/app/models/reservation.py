from sqlalchemy import Integer, String, Index
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.core.database import BaseModel
from app.models.device import Device
from app.models.lab import Lab
from app.models.user import User


class Reservation(BaseModel):
    """预约模型"""
    __tablename__ = "reservations"
    __table_args__ = (
        Index("idx_user_lab_device", "user_id", "lab_id", "device_id"),
        {"comment": "预约表"}
    )

    user_id: Mapped[int] = mapped_column(Integer, comment="用户ID", server_default="0", nullable=False)
    lab_id: Mapped[int] = mapped_column(Integer, comment="实验室ID", server_default="0", nullable=False)
    device_id: Mapped[int] = mapped_column(Integer, comment="设备ID", server_default="0", nullable=False)
    date: Mapped[str] = mapped_column(String(32), server_default="", comment="预约日期", nullable=False)
    start_time: Mapped[str] = mapped_column(String(32), server_default="", comment="预约开始时间", nullable=False)
    end_time: Mapped[str] = mapped_column(String(32), server_default="", comment="预约结束时间", nullable=False)
    remark: Mapped[str | None] = mapped_column(String(255), server_default="", comment="预约备注", nullable=False)
    status: Mapped[int] = mapped_column(Integer, comment="预约状态,0待审核，1已通过，-1已拒绝，-2已取消",
                                        server_default="0", nullable=False)

    user: Mapped[User] = relationship(primaryjoin="Reservation.user_id == User.id", foreign_keys="Reservation.user_id",
                                      lazy="selectin", )
    lab: Mapped[Lab] = relationship(primaryjoin="Reservation.lab_id == Lab.id", foreign_keys="Reservation.lab_id",
                                    lazy="selectin", )
    device: Mapped[Device] = relationship(primaryjoin="Reservation.device_id == Device.id",
                                          foreign_keys="Reservation.device_id", lazy="selectin", )
