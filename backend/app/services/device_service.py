from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.common.exceptions import BizException
from app.common.response import PageResponse
from app.models.device import Device
from app.schemas.device import DeviceRes, DeviceCreateRequest, DeviceUpdateRequest


def get_device_list(db: Session, keyword: str | None = None, lab_id: int | None = None, page: int = 1,
                    page_size: int = 10):
    """获取设备分页列表"""
    offset = (page - 1) * page_size
    query = db.query(Device)

    if keyword:
        query = query.filter(
            or_(
                Device.name.like(f"%{keyword}%"),
                Device.description.like(f"%{keyword}%"),
            )
        )
    if lab_id:
        query = query.filter(Device.lab_id == lab_id)

    total = query.count()
    devices = query.order_by(Device.id.desc()).offset(offset).limit(page_size).all()

    lists = []
    for device in devices:
        data = DeviceRes.model_validate(device)
        data.lab_name = device.lab.name if device.lab else None
        lists.append(data)

    return PageResponse(
        list=lists,
        total=total,
    )


def create_device(db: Session, data: DeviceCreateRequest):
    """创建设备"""
    device = db.query(Device).filter(Device.name == data.name).first()
    if device:
        raise BizException(msg="设备名称已存在")

    create_data = data.model_dump(exclude_unset=True)

    device = Device()
    for key, value in create_data.items():
        setattr(device, key, value)

    db.add(device)
    db.commit()
    db.refresh(device)
    return DeviceRes.model_validate(device)


def update_device(db: Session, id: int, data: DeviceUpdateRequest):
    """更新设备信息"""
    device = db.query(Device).filter(Device.id == id).first()
    if not device:
        raise BizException(msg="设备不存在")

    if data.name:
        if db.query(Device).filter(Device.name == data.name).filter(Device.id != id).first():
            raise BizException(msg="设备名称已存在")

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(device, key, value)

    db.commit()
    db.refresh(device)
    return DeviceRes.model_validate(device)


def delete_device(db: Session, id: int):
    """删除设备"""
    device = db.query(Device).filter(Device.id == id).first()
    if not device:
        raise BizException(msg="设备不存在")
    db.delete(device)
    db.commit()
