from datetime import datetime

from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import create_engine, DateTime

from app.config.config import settings

# 数据库引擎
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
)

# 数据库会话工厂
SessionLocal = sessionmaker(engine, autoflush=False)


# 获取数据库
def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class BaseModel(DeclarativeBase):
    """基础模型"""
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="主键ID", sort_order=-1)
    created: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间", sort_order=99998)
    updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间",
                                              sort_order=99999)
