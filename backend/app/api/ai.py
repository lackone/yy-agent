import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import StreamingResponse

from app.common.response import Response
from app.core.database import get_db
from app.deps.check_user import get_current_user
from app.models.user import User
from app.schemas.ai import ChatRequest, ChatMessage
from app.services import ai_service, agent_service

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/chat")
def chat(messages: ChatRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """AI聊天"""
    # res = ai_service.chat(db, user, messages)
    res = agent_service.run_agent(db, user, messages)
    return Response.success(data=ChatMessage(
        role="assistant",
        content=res,
    ))


@router.post("/chat/stream")
async def stream_chat(messages: ChatRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """流式AI聊天"""

    async def event_gen():
        async for event in agent_service.stream_agent(db, user, messages):
            yield f"data: {json.dumps(event, ensure_ascii=False)}\n\n"

    return StreamingResponse(event_gen(),
                             media_type="text/event-stream",
                             headers={
                                 "Cache-Control": "no-cache",
                                 "Connection": "keep-alive",
                                 "X-Accel-Buffering": "no"
                             })
