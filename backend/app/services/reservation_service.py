import asyncio
from datetime import datetime

from sqlalchemy import or_, and_
from sqlalchemy.orm import Session

from app.common.exceptions import BizException
from app.common.response import PageResponse
from app.core.database import SessionLocal
from app.models.device import Device
from app.models.lab import Lab
from app.models.reservation import Reservation
from app.models.user import User
from app.schemas.reservation import ReservationCreateRequest, ReservationResponse


def get_reservation_list(db: Session, user: User, status: int | None = None, page: int = 1,
                         page_size: int = 10):
    """获取预约分页列表"""
    offset = (page - 1) * page_size
    query = db.query(Reservation)

    if user:
        query = query.filter(Reservation.user_id == user.id)
    if status is not None:
        query = query.filter(Reservation.status == status)

    total = query.count()
    reservations = query.order_by(Reservation.id.desc()).offset(offset).limit(page_size).all()

    lists = []
    for reservation in reservations:
        data = ReservationResponse.model_validate(reservation)
        data.user_name = reservation.user.username if reservation.user else None
        data.lab_name = reservation.lab.name if reservation.lab else None
        data.device_name = reservation.device.name if reservation.device else None
        data.type = "设备" if reservation.device_id else "实验室"
        lists.append(data)

    return PageResponse(
        list=lists,
        total=total,
    )


def get_reservation(db: Session, reservation_id: int):
    """获取预约详情"""
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise BizException("预约不存在")
    return ReservationResponse.model_validate(reservation)


def create_reservation(db: Session, user: User, data: ReservationCreateRequest):
    """创建预约"""
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M")
    if data.date < current_date:
        raise BizException("预约日期不能早于当前日期")
    if data.date == current_date and data.end_time < current_time:
        raise BizException("预约结束时间不能早于当前时间")
    if data.end_time < data.start_time:
        raise BizException("预约结束时间不能早于预约开始时间")

    lab = db.query(Lab).filter(Lab.id == data.lab_id).first()
    if not lab:
        raise BizException("实验室不存在")
    if lab.status != 1:
        raise BizException("实验室状态异常")
    if lab.open_time and data.start_time < lab.open_time:
        raise BizException("预约时间不能早于实验室开放时间")
    if lab.close_time and data.end_time > lab.close_time:
        raise BizException("预约时间不能晚于实验室关闭时间")

    if data.device_id:
        device = db.query(Device).filter(Device.id == data.device_id).first()
        if not device:
            raise BizException("设备不存在")
        if device.status != 1:
            raise BizException("设备状态异常")

    # 检查预约时间冲突
    query = db.query(Reservation).filter(
        Reservation.lab_id == data.lab_id,
        Reservation.date == data.date,
        Reservation.status.in_([0, 1]),
        Reservation.start_time < data.end_time,
        Reservation.end_time > data.start_time,
    )

    if data.device_id:
        query = query.filter(Reservation.device_id == data.device_id)
    else:
        query = query.filter(Reservation.device_id.is_(None))

    if query.first():
        raise BizException("预约时间冲突")

    create_data = data.model_dump(exclude_unset=True)

    reservation = Reservation()
    for key, value in create_data.items():
        setattr(reservation, key, value)

    reservation.user_id = user.id

    db.add(reservation)
    db.commit()
    db.refresh(reservation)


def cancel_reservation(db: Session, user: User, reservation_id: int):
    """取消预约"""
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise BizException("预约不存在")
    if reservation.user_id != user.id:
        raise BizException("预约不属于用户")
    if reservation.status != 0:
        raise BizException("当前预约状态不能取消")

    reservation.status = -2
    db.commit()
    db.refresh(reservation)

    return ReservationResponse.model_validate(reservation)


def audit_reservation(db: Session, user: User, reservation_id: int, status: int):
    """审核预约"""
    if status not in [1, -1]:
        raise BizException("审核状态异常")
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise BizException("预约不存在")
    if reservation.status != 0:
        raise BizException("当前预约状态不能审核")

    reservation.status = status
    db.commit()
    db.refresh(reservation)

    return ReservationResponse.model_validate(reservation)


def expire_reservation():
    """过期预约"""
    db = SessionLocal()
    try:
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M")

        reservations = db.query(Reservation).filter(
            Reservation.status == 0,
            or_(
                Reservation.date < today,
                and_(
                    Reservation.date == today,
                    Reservation.end_time <= time
                ).self_group(),
            ),
        ).all()

        changed = False
        for reservation in reservations:
            reservation.status = -2
            changed = True

        if changed:
            db.commit()

    finally:
        db.close()


async def run_expire_reservation():
    """运行过期预约任务"""
    try:
        while True:
            print("运行过期预约任务")
            await asyncio.to_thread(expire_reservation)
            await asyncio.sleep(60)
    except asyncio.CancelledError:
        return
