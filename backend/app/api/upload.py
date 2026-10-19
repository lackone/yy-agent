import os
import shutil
import time
import uuid
from pathlib import Path

from fastapi import APIRouter, UploadFile, File

from app.common.exceptions import BizException
from app.common.response import Response
from app.config.config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE, UPLOADS_DIR
from app.schemas.file import FileRes

router = APIRouter(prefix="/upload", tags=["上传"])


@router.post("/file")
def upload_file(file: UploadFile = File(...)):
    """上传文件"""
    if not file.filename:
        raise BizException(msg="文件名不能为空")

    # 校验文件扩展名
    original_name = os.path.basename(file.filename)
    ext = Path(original_name).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise BizException(msg=f"文件扩展名{ext}不支持")

    # 校验文件大小
    if file.size and file.size > MAX_FILE_SIZE:
        raise BizException(msg=f"文件大小不能超过{MAX_FILE_SIZE // 1024 // 1024}MB")

    # 生成文件名
    timestamp = int(time.time() * 1000)
    new_name = f"{timestamp}_{uuid.uuid4().hex[:8]}{ext}"
    year_month = time.strftime("%Y%m", time.localtime())
    day = time.strftime("%d", time.localtime())
    save_path = UPLOADS_DIR / year_month / day / new_name
    save_path.parent.mkdir(parents=True, exist_ok=True)

    # 保存文件
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return Response.success(msg="上传成功", data=FileRes(
        original_name=original_name,
        new_name=new_name,
        size=file.size,
        url=f"/uploads/{year_month}/{day}/{new_name}"
    ))
