#agent_router.py

# 사용자 요청을 받아서 → agent_service로 전달하는 역할 (라우터 = API 입구)

from fastapi import APIRouter
from schemas.study_schema import StudyRequest # 요청 데이터 형식을 정의한 Pydantic 모델
from services import agent_service 

router = APIRouter() # 라우터 객체 생성 (여기에 API들을 등록함)

@router.post("/agent") 
# 클라이언트가 POST 방식으로 "/agent" 경로로 요청을 보내면 아래 함수 실행

def run_agent(request: StudyRequest): 
    # 요청 body(JSON)를 StudyRequest 형태로 자동 변환하여 request 변수에 담음
    # → request는 dict가 아니라 Pydantic 객체이므로 request.message 형태로 접근 가능
    # request.message = 사용자가 보낸 데이터 중에서 "message" 값만 꺼냄
    
    return agent_service.run(
        message=request.message,
        study_mode=request.study_mode #사용자가 입력한 학습 요청 전달
        )
        
    # request에서 message 값을 꺼내서 agent_service의 run 함수에 전달
    # → 실제 AI 처리(LLM 호출 등)는 service에서 수행됨
    # → 실행 결과를 그대로 클라이언트에게 응답으로 반환