from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.common.exceptions import BizException
from app.common.response import PageResponse
from app.models.lab import Lab
from app.schemas.lab import LabRes, LabCreateRequest, LabUpdateRequest


def get_lab_list(db: Session, keyword: str | None = None, status: int | None = None, page: int = 1,
                 page_size: int = 10):
    """获取实验室分页列表"""
    offset = (page - 1) * page_size
    query = db.query(Lab)

    if keyword:
        query = query.filter(
            or_(
                Lab.name.like(f"%{keyword}%"),
                Lab.description.like(f"%{keyword}%"),
            )
        )

    if status is not None:
        query = query.filter(Lab.status == status)

    total = query.count()
    labs = query.order_by(Lab.id.desc()).offset(offset).limit(page_size).all()

    return PageResponse(
        list=[LabRes.model_validate(lab) for lab in labs],
        total=total,
    )


def get_lab(db: Session, id: int):
    """获取实验室详情"""
    lab = db.query(Lab).filter(Lab.id == id).first()
    if not lab:
        raise BizException(msg="实验室不存在")
    return LabRes.model_validate(lab)


def create_lab(db: Session, data: LabCreateRequest):
    """创建实验室"""
    lab = db.query(Lab).filter(Lab.name == data.name).first()
    if lab:
        raise BizException(msg="实验室名称已存在")

    create_data = data.model_dump(exclude_unset=True)

    lab = Lab()
    for key, value in create_data.items():
        setattr(lab, key, value)

    db.add(lab)
    db.commit()
    db.refresh(lab)
    return LabRes.model_validate(lab)


def update_lab(db: Session, id: int, data: LabUpdateRequest):
    """更新实验室信息"""
    lab = db.query(Lab).filter(Lab.id == id).first()
    if not lab:
        raise BizException(msg="实验室不存在")

    if data.name:
        if db.query(Lab).filter(Lab.name == data.name).filter(Lab.id != id).first():
            raise BizException(msg="实验室名称已存在")

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(lab, key, value)

    db.commit()
    db.refresh(lab)
    return LabRes.model_validate(lab)


def delete_lab(db: Session, id: int):
    """删除实验室"""
    lab = db.query(Lab).filter(Lab.id == id).first()
    if not lab:
        raise BizException(msg="实验室不存在")
    db.delete(lab)
    db.commit()
