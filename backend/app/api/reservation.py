from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.response import Response
from app.core.database import get_db
from app.deps.check_user import get_current_user
from app.models.user import User
from app.schemas.reservation import ReservationCreateRequest, AuditReservationRequest
from app.services import reservation_service

router = APIRouter(prefix="/reservation", tags=["预约"])


@router.post("")
def create_reservation(data: ReservationCreateRequest, user: User = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    """创建预约"""
    reservation_service.create_reservation(db, user, data)
    return Response.success(msg="预约成功")


@router.get("/list")
def get_reservation_list(user: User = Depends(get_current_user), status: int | None = None, page: int = 1,
                         page_size: int = 10, db: Session = Depends(get_db)):
    """获取预约分页列表"""
    res = reservation_service.get_reservation_list(db, user, status, page, page_size)
    return Response.success(data=res)


@router.get("/{id}")
def get_reservation(id: int, db: Session = Depends(get_db)):
    """获取预约详情"""
    res = reservation_service.get_reservation(db, id)
    return Response.success(data=res)


@router.put("/{id}/cancel")
def cancel_reservation(id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """取消预约"""
    res = reservation_service.cancel_reservation(db, user, id)
    return Response.success(data=res)


@router.put("/{id}/audit")
def audit_reservation(id: int, data: AuditReservationRequest, user: User = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    """审核预约"""
    res = reservation_service.audit_reservation(db, user, id, data.status)
    return Response.success(data=res)
