from datetime import datetime, timedelta, timezone

import jwt

from app.config.config import settings


def gen_token(id: int):
    """生成JWT"""

    expire = datetime.now(timezone.utc) + timedelta(hours=settings.JWT_EXPIRE_HOURS)

    payload = {
        "id": id,
        "exp": expire,
        "user_id": id,
    }

    return jwt.encode(
        payload,
        settings.JWT_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def parse_token(token: str):
    """解析JWT"""

    return jwt.decode(token, settings.JWT_KEY, algorithms=[settings.JWT_ALGORITHM])
