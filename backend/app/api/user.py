from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.response import Response
from app.core.database import get_db
from app.deps.check_user import get_current_user
from app.models.user import User
from app.schemas.user import UserUpdateRequest, UserPwdChgReq, UserCreateRequest
from app.services import user_service

router = APIRouter(prefix="/user", tags=["用户"])


@router.get("/me")
def get_me(user: User = Depends(get_current_user)):
    """获取用户信息"""
    res = user_service.get_me(user)
    return Response.success(data=res)


@router.put("/me")
def update_me(data: UserUpdateRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """更新用户信息"""
    res = user_service.update_me(db, user, data)
    return Response.success(data=res)


@router.put("/password")
def update_password(data: UserPwdChgReq, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """修改用户密码"""
    res = user_service.update_password(db, user, data)
    return Response.success(data=res)


@router.get("/list")
def get_user_list(keyword: str | None = None, page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    """获取用户分页列表"""
    res = user_service.get_user_list(db, keyword, page, page_size)
    return Response.success(data=res)


@router.post("")
def create_user(user: UserCreateRequest, db: Session = Depends(get_db)):
    """创建用户"""
    res = user_service.create_user(db, user)
    return Response.success(data=res)


@router.put("/{id}")
def update_user(id: int, user: UserUpdateRequest, db: Session = Depends(get_db)):
    """更新用户"""
    res = user_service.update_user(db, id, user)
    return Response.success(data=res)


@router.delete("/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    """删除用户"""
    user_service.delete_user(db, id)
    return Response.success()
