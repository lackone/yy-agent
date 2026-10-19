from sqlalchemy.orm import Session

from app.common.exceptions import BizException
from app.models.user import User
from app.schemas.login import LoginReq, LoginRes
from app.schemas.register import RegisterRes, RegisterReq
from app.utils.password import check_password, hash_password
from app.utils.token import gen_token


def login(db: Session, data: LoginReq):
    """登录"""
    user = db.query(User).filter(User.account == data.account).first()
    if not user:
        raise BizException(msg="账号不存在")
    if user.status != 1:
        raise BizException(msg="账号禁用")
    if not check_password(data.password, user.password):
        raise BizException(msg="密码错误")

    res = LoginRes.model_validate(user)
    token = gen_token(user.id)
    res.token = token

    return res


def register(db: Session, data: RegisterReq):
    """注册"""
    user = db.query(User).filter(User.account == data.account).first()
    if user:
        raise BizException(msg="账号已存在")
    if data.password != data.repassword:
        raise BizException(msg="两次密码不一致")

    user = User(
        account=data.account,
        username=data.account,
        password=hash_password(data.password),
        status=1,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
