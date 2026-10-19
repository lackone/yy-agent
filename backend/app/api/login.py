from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.response import Response
from app.core.database import get_db
from app.schemas.login import LoginReq, LoginRes
from app.schemas.register import RegisterReq
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["登录"])


@router.post("/login")
def login(data: LoginReq, db: Session = Depends(get_db)):
    """登录"""
    res = auth_service.login(db, data)

    return Response.success(data=res)


@router.post("/register")
def register(data: RegisterReq, db: Session = Depends(get_db)):
    """注册"""
    auth_service.register(db, data)

    return Response.success(msg="注册成功")
