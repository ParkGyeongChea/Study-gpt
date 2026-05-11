
# side_chat_router.py

# 사이드챗 API 라우터
# 프론트에서 사이드챗 질문을 보내면,
# 이 파일이 요청을 받고 side_chat_service.py로 넘겨준다.

from fastapi import APIRouter
from pydantic import BaseModel
from services.side_chat_service import generate_side_chat


router = APIRouter()


class SideChatRequest(BaseModel):
    # 사용자가 사이드챗에 보내는 데이터 구조
    # 예시: {"message": "사과 영어 스펠링이 뭐야?"}
    message: str


class SideChatResponse(BaseModel):
    # 서버가 사이드챗 응답으로 돌려줄 데이터 구조
    # 예시: {"message": "사과의 영어 스펠링은 apple 입니다."}
    message: str


@router.post("/side-chat", response_model=SideChatResponse)
# 사이드챗 질문을 처리하는 API
# POST /side-chat 요청을 받는다.
def side_chat(request: SideChatRequest):

    message = request.message
    # 사용자가 보낸 JSON 데이터에서 message 값만 꺼냄

    result = generate_side_chat(message)
    # 꺼낸 message를 side_chat_service.py의 generate_side_chat 함수로 넘김
    # generate_side_chat 함수는 GPT에게 질문을 보내고 답변 문자열을 반환함

    return {
        "message": result
    }
    # response_model=SideChatResponse 구조에 맞게
    # {"message": "..."} 형태로 반환
