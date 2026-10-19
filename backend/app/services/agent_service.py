from typing import Any

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from langgraph.constants import START
from langgraph.graph import MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from sqlalchemy.orm import Session
from langchain.chat_models import init_chat_model

from app.common.exceptions import BizException
from app.config.config import settings
from app.models.user import User
from app.schemas.ai import ChatRequest
from app.services import agent_tools

SYSTEM_PROMPT = """你是智能实验室预约系统的 Agent，回答要简洁。
你可以使用以下工具：
1、使用 search_lab_docs 检索知识库中的信息，查询实验室的规则，安全，开放时间等问题
2、使用 list_open_labs 查询开放实验室
3、使用 list_lab_devices 查询实验室设备
4、用户进行预约确认后，使用 create_reservation 来创建预约
5、使用 get_today 获取当前日期

在提交预约之前必须向用户复述：实验室ID与名称，或设备ID与名称，日期，开始时间，结束时间。并得到用户确认再进行实际操作。
用户没说【确认】【确认预约】【就这样预约】等确定性回复之前，不要调用 create_reservation 工具。
工作流的确认环节里如果缺少了 lab_id，请先 list_open_labs 查到了 lab_id 再创建，不要瞎写。
工作流的确认环节里如果缺少了 device_id，请先 list_lab_devices 查到了 device_id 再创建，不要瞎写。

预约成功后状态是待审核，必须管理员确认后实验室(或设备)才能使用。
不要瞎编数据库里没有的实验室或者设备信息。
如果是问开放时间或者实验室规则，优先调用 search_lab_docs，不要凭空回复
"""

TOOL_LABELS = {
    "search_lab_docs": "检索知识库中的信息",
    "list_open_labs": "查询开放实验室",
    "list_lab_devices": "查询实验室设备",
    "create_reservation": "创建预约",
    "get_today": "获取当前日期",
}


def build_agent(db: Session, user: User):
    """构建智能体"""
    tools = agent_tools.build_tools(db, user)

    llm = init_chat_model(
        model=settings.LLM_MODEL,
        model_provider="openai",
        api_key=settings.API_KEY,
        base_url=settings.BASE_URL,
        temperature=0,
        streaming=True  # 开启流式输出
    ).bind_tools(tools)

    async def agent_node(state: MessagesState):
        """智能体节点"""
        response = await llm.ainvoke(state["messages"])
        # response = llm.invoke(state["messages"])
        return {"messages": [response]}

    graph = StateGraph(MessagesState)
    graph.add_node("agent", agent_node)
    graph.add_node("tools", ToolNode(tools))

    graph.add_edge(START, "agent")
    # 智能体节点根据条件选择调用工具节点或结束
    graph.add_conditional_edges("agent", tools_condition)
    # 让 agent 看 tool 调用的结果
    graph.add_edge("tools", "agent")

    return graph.compile()


def _build_history(data: ChatRequest):
    """构建历史记录"""

    if not data.messages:
        raise BizException("messages is not set")

    history = []
    for message in data.messages:
        if message.role == "user" and message.content.strip():
            history.append(HumanMessage(content=message.content))
        elif message.role == "assistant" and message.content.strip():
            history.append(AIMessage(content=message.content))
    if not history:
        raise BizException("history is empty")

    return history


def _tool_output_preview(output: Any, limit: int = 200):
    """工具工具输出预览"""
    if isinstance(output, ToolMessage):
        output = output.content

    text = output if isinstance(output, str) else str(output)

    return text if len(text) <= limit else text[:limit] + "..."


def _chunk_text(chunk: Any):
    """处理流式输出的 chunk"""
    if chunk is None:
        return ""

    content = getattr(chunk, "content", None)
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for part in content:
            if isinstance(part, str):
                parts.append(part)
            elif isinstance(part, dict):
                parts.append(part.get("text") or "")
        return "".join(parts)

    return str(content) if content is not None else ""


async def stream_agent(db: Session, user: User, data: ChatRequest):
    """流式智能体"""
    try:
        history = _build_history(data)
        agent = build_agent(db, user)
        inputs = {
            "messages": [
                SystemMessage(content=SYSTEM_PROMPT),
                *history
            ]
        }
        yield {"type": "status", "message": "正在思考..."}

        async for event in agent.astream_events(inputs, version="v2", config={"recursion_limit": 10}):
            kind = event.get("event")
            if kind == "on_tool_start":
                name = event.get("name") or ""
                yield {
                    "type": "tool_start",
                    "name": name,
                    "label": TOOL_LABELS.get(name, name)
                }
            elif kind == "on_tool_end":
                name = event.get("name") or ""
                yield {
                    "type": "tool_end",
                    "name": name,
                    "label": TOOL_LABELS.get(name, name),
                    "preview": _tool_output_preview((event.get("data") or {}).get("output"))
                }
            elif kind == "on_chat_model_stream":
                metadata = event.get("metadata") or {}
                if metadata.get("langgraph_node") not in (None, "agent"):
                    continue
                text = _chunk_text((event.get("data") or {}).get("chunk"))
                yield {
                    "type": "token",
                    "content": text
                }

        yield {"type": "done"}
    except Exception as e:
        yield {"type": "error", "message": str(e)}


def run_agent(db: Session, user: User, data: ChatRequest):
    """运行智能体"""
    try:
        history = _build_history(data)
        agent = build_agent(db, user)
        inputs = {
            "messages": [
                SystemMessage(content=SYSTEM_PROMPT),
                *history
            ],
        }
        response = agent.invoke(inputs, config={"recursion_limit": 10})
    except Exception as e:
        raise BizException(str(e))

    messages = response.get("messages") or []

    if not messages:
        raise BizException("messages is empty")

    for message in reversed(messages):
        if isinstance(message, AIMessage) and message.content.strip():
            content = message.content.strip()
            if isinstance(content, list):
                content = "".join(
                    part.get("text", "") if isinstance(part, dict) else str(part)
                    for part in content
                )
            if str(content).strip():
                return str(content).strip()
