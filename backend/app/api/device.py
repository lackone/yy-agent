from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.response import Response
from app.core.database import get_db
from app.schemas.device import DeviceCreateRequest, DeviceUpdateRequest
from app.services import device_service

router = APIRouter(prefix="/device", tags=["设备"])


@router.get("/list")
def get_device_list(keyword: str | None = None, lab_id: int | None = None, page: int = 1, page_size: int = 10,
                    db: Session = Depends(get_db)):
    """获取设备分页列表"""
    res = device_service.get_device_list(db, keyword, lab_id, page, page_size)
    return Response.success(data=res)


@router.post("")
def create_device(device: DeviceCreateRequest, db: Session = Depends(get_db)):
    """创建设备"""
    res = device_service.create_device(db, device)
    return Response.success(data=res)


@router.put("/{id}")
def update_device(id: int, device: DeviceUpdateRequest, db: Session = Depends(get_db)):
    """更新设备"""
    res = device_service.update_device(db, id, device)
    return Response.success(data=res)


@router.delete("/{id}")
def delete_device(id: int, db: Session = Depends(get_db)):
    """删除设备"""
    device_service.delete_device(db, id)
    return Response.success()
