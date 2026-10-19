import json

from openai import OpenAI
from openai.types.beta.threads.runs import tool_call
from sqlalchemy.orm import Session

from app.common.exceptions import BizException
from app.config.config import settings
from app.models.user import User
from app.schemas.ai import ChatRequest, ChatMessage
from app.services import kb_service, lab_service, device_service

SYSTEM_PROMPT = """你是智能实验室预约系统的助手，回答要简洁。
如果下面提供了实验室资料，请依据资料回答规则、安全、文档里的开放时间说明。
查询当前有哪些开放实验室、某实验室有哪些设备时，必须调用工具，不要编造。
你不能替用户提交预约，也不能直接改数据库。
如果用户要预约，请说明去「实验室列表」选择后提交，等待管理员审核。
"""

TOOL = [
    {
        "type": "function",
        "function": {
            "name": "list_open_labs",
            "description": "列出所有开放的实验室",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "关键词，用于筛选实验室的名称"
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_lab_devices",
            "description": "列出实验室的所有设备",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab_id": {
                        "type": "integer",
                        "description": "实验室的ID"
                    },
                    "keyword": {
                        "type": "string",
                        "description": "关键词，用于筛选设备的名称"
                    }
                }
            }
        }
    }
]


def get_client() -> OpenAI:
    """获取AI客户端"""
    if not settings.API_KEY:
        raise BizException("API_KEY is not set")
    if not settings.BASE_URL:
        raise BizException("BASE_URL is not set")

    return OpenAI(api_key=settings.API_KEY, base_url=settings.BASE_URL)


def chat(db: Session, user: User, data: ChatRequest):
    """与AI聊天"""
    if not data.messages:
        raise BizException("messages is not set")

    history = []
    for message in data.messages:
        if message.role in ("user", "assistant") and message.content.strip():
            history.append(message.model_dump())
    if not history:
        raise BizException("history is empty")

    # 从历史记录中提取用户最新的问题
    question = next(
        (item["content"] for item in reversed(history) if item["role"] == "user"),
        ""
    )

    kb = kb_service.search(question)
    system_prompt = SYSTEM_PROMPT
    if kb:
        system_prompt += f"\n\n以下是检索到的实验室的资料:\n{kb}"

    print(system_prompt)

    client = get_client()
    messages = [
        ChatMessage(role="assistant", content=system_prompt),
        *history
    ]

    try:
        for _ in range(3):
            response = client.chat.completions.create(
                model=settings.LLM_MODEL,
                messages=messages,
                tools=TOOL,
                tool_choice="auto",
            )

            message = response.choices[0].message
            print(message)

            tool_calls = message.tool_calls or []
            if not tool_calls:
                content = message.content
                if not content or not content.strip():
                    raise BizException("message content is empty")
                return message

            messages.append({
                "role": "assistant",
                "content": message.content,
                "tool_calls": [
                    {
                        "id": call.id,
                        "type": "function",
                        "function": {
                            "name": call.function.name,
                            "arguments": call.function.arguments,
                        }
                    } for call in tool_calls
                ],
            })

            for call in tool_calls:
                result = run_tool(db, call.function.name, call.function.arguments)
                messages.append({
                    "role": "tool",
                    "content": result,
                    "tool_call_id": call.id,
                })

    except Exception as e:
        raise BizException(f"对话失败 {str(e)}")


def run_tool(db: Session, func: str, args: str):
    """运行工具"""
    try:
        args = json.loads(args or "{}")
    except Exception as e:
        raise BizException(f"参数解析失败 {str(e)}")

    try:
        if func == "list_open_labs":
            keyword = args.get("keyword", "").strip()

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

        if func == "list_lab_devices":
            lab_id = args.get("lab_id", 0)
            keyword = args.get("keyword", "").strip()

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
        raise BizException(f"工具调用失败 {str(e)}")
