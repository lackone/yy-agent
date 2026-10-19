from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.response import Response
from app.core.database import get_db
from app.schemas.lab import LabCreateRequest, LabUpdateRequest
from app.services import lab_service

router = APIRouter(prefix="/lab", tags=["实验室"])


@router.get("/list")
def get_lab_list(keyword: str | None = None, status: int | None = None, page: int = 1, page_size: int = 10,
                 db: Session = Depends(get_db)):
    """获取实验室分页列表"""
    res = lab_service.get_lab_list(db, keyword, status, page, page_size)
    return Response.success(data=res)


@router.get("/{id}")
def get_lab(id: int, db: Session = Depends(get_db)):
    """获取实验室详情"""
    res = lab_service.get_lab(db, id)
    return Response.success(data=res)


@router.post("")
def create_lab(lab: LabCreateRequest, db: Session = Depends(get_db)):
    """创建实验室"""
    res = lab_service.create_lab(db, lab)
    return Response.success(data=res)


@router.put("/{id}")
def update_lab(id: int, lab: LabUpdateRequest, db: Session = Depends(get_db)):
    """更新实验室"""
    res = lab_service.update_lab(db, id, lab)
    return Response.success(data=res)


@router.delete("/{id}")
def delete_lab(id: int, db: Session = Depends(get_db)):
    """删除实验室"""
    lab_service.delete_lab(db, id)
    return Response.success()
