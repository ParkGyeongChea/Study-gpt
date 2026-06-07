
# side_chat_router.py

# 사이드챗 API 라우터
# 프론트에서 사이드챗 질문을 보내면,
# 이 파일이 요청을 받고 side_chat_service.py로 넘겨준다.

from fastapi import APIRouter
from pydantic import BaseModel
from services.side_chat_service import generate_side_chat


router = APIRouter()


class SideChatRequest(BaseModel):
    message: str


class SideChatResponse(BaseModel):
    message: str


@router.post("/side-chat", response_model=SideChatResponse)

def side_chat(request: SideChatRequest):
    message = request.message
    result = generate_side_chat(message)
    
    return {
        "message": result
    }
    
