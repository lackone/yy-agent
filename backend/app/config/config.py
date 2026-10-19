from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# 后端项目根路径
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# 上传目录
UPLOADS_DIR = BASE_DIR / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
MAX_FILE_SIZE = 100 * 1024 * 1024
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".svg", ".pdf", ".docx", ".doc", ".xlsx",
                      ".xls"}


class Settings(BaseSettings):
    """配置模型"""
    DATABASE_URL: str

    JWT_KEY: str
    JWT_EXPIRE_HOURS: int = 24
    JWT_ALGORITHM: str = "HS256"

    DEBUG: bool = True

    BASE_URL: str
    API_KEY: str
    LLM_MODEL: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8"
    )


settings = Settings()
