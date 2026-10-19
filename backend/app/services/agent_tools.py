import json
from datetime import datetime

from langchain_core.tools import tool
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.reservation import ReservationCreateRequest
from app.services import kb_service, lab_service, device_service, reservation_service


def build_tools(db: Session, user: User):
    """构建智能体工具"""

    @tool
    def search_lab_docs(query: str = ""):
        """根据用户的提问检索知识库"""
        try:
            return kb_service.search(query)
        except Exception as e:
            return json.dumps({
                "ok": False,
                "error": f"{str(e)}",
            })

    @tool
    def list_open_labs(keyword: str = ""):
        """查询开放实验室"""
        try:
            keyword = keyword.strip()

            list = lab_service.get_lab_list(db, keyword=keyword, page=1, page_size=10, status=1)
            rows = [
                {
                    "id": item.id,
                    "name": item.name,
                    "location": item.location,
                    "capacity": item.capacity,
                    "open_time": item.open_time,
                    "close_time": item.close_time,
                } for item in list.list
            ]
            return json.dumps({
                "total": list.total,
                "labs": rows,
            })
        except Exception as e:
            return json.dumps({
                "ok": False,
                "error": f"{str(e)}",
            })

    @tool
    def list_lab_devices(lab_id: int, keyword: str = ""):
        """查询实验室设备"""
        try:
            keyword = keyword.strip()

            list = device_service.get_device_list(db, keyword=keyword, lab_id=int(lab_id), page=1, page_size=10)
            rows = [
                {
                    "id": item.id,
                    "name": item.name,
                    "lab_id": item.lab_id,
                    "lab_name": item.lab_name,
                    "description": item.description,
                    "spec": item.spec,
                    "quantity": item.quantity,
                } for item in list.list
            ]
            return json.dumps({
                "total": list.total,
                "devices": rows,
            })
        except Exception as e:
            return json.dumps({
                "ok": False,
                "error": f"{str(e)}",
            })

    @tool
    def create_reservation(lab_id: int,
                           date: str,
                           start_time: str,
                           end_time: str,
                           device_id: int | None = None,
                           remark: str | None = None):
        """创建实验室预约或设备预约"""
        try:
            data = ReservationCreateRequest(
                lab_id=lab_id,
                device_id=device_id,
                date=date,
                start_time=start_time,
                end_time=end_time,
                remark=remark,
            )
            reservation_service.create_reservation(db, user, data)

            return json.dumps({
                "ok": True,
                "message": "预约成功",
                "lab_id": lab_id,
                "device_id": device_id,
                "date": date,
                "start_time": start_time,
                "end_time": end_time,
            })
        except Exception as e:
            return json.dumps({
                "ok": False,
                "error": f"{str(e)}",
            })

    @tool
    def get_today():
        """获取当前日期"""
        return datetime.now().strftime("%Y-%m-%d")

    return [
        search_lab_docs,
        list_open_labs,
        list_lab_devices,
        create_reservation,
        get_today,
    ]
