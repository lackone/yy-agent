from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.common.exceptions import BizException
from app.common.response import PageResponse
from app.models.user import User
from app.schemas.user import UserRes, UserUpdateRequest, UserPwdChgReq, UserCreateRequest, UserDeleteRequest
from app.utils.password import check_password, hash_password


def get_me(user: User):
    """获取用户信息"""
    return UserRes.model_validate(user)


def update_me(db: Session, user: User, data: UserUpdateRequest):
    """更新用户信息"""
    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return UserRes.model_validate(user)


def update_password(db: Session, user: User, data: UserPwdChgReq):
    """修改用户密码"""
    if not check_password(data.old_password, user.password):
        raise BizException(msg="旧密码错误")
    if data.new_password == data.old_password:
        raise BizException(msg="新密码不能与旧密码相同")
    if data.new_password != data.confirm_password:
        raise BizException(msg="两次输入密码不一致")

    user.password = hash_password(data.new_password)
    db.commit()
    db.refresh(user)
    return UserRes.model_validate(user)


def get_user_list(db: Session, keyword: str | None = None, page: int = 1, page_size: int = 10):
    """获取用户分页列表"""
    offset = (page - 1) * page_size
    query = db.query(User)

    if keyword:
        query = query.filter(
            or_(
                User.username.like(f"%{keyword}%"),
                User.account.like(f"%{keyword}%"),
            )
        )

    total = query.count()
    users = query.order_by(User.id.desc()).offset(offset).limit(page_size).all()

    return PageResponse(
        list=[UserRes.model_validate(user) for user in users],
        total=total,
    )


def create_user(db: Session, data: UserCreateRequest):
    """创建用户"""
    user = db.query(User).filter(User.account == data.account).first()
    if user:
        raise BizException(msg="账号已存在")

    create_data = data.model_dump(exclude_unset=True)

    user = User()
    for key, value in create_data.items():
        setattr(user, key, value)

    user.password = hash_password(user.password)

    db.add(user)
    db.commit()
    db.refresh(user)
    return UserRes.model_validate(user)


def update_user(db: Session, id: int, data: UserUpdateRequest):
    """更新用户信息"""
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise BizException(msg="用户不存在")

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        if key == "password":
            value = hash_password(value)
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return UserRes.model_validate(user)


def delete_user(db: Session, id: int):
    """删除用户"""
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise BizException(msg="用户不存在")
    db.delete(user)
    db.commit()
