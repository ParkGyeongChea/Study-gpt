#agent_router.py

# 사용자 요청을 받아서 → agent_service로 전달하는 역할 (라우터 = API 입구)

from fastapi import APIRouter, Depends #Depends= 필요한 기능 자동 실행 기능
from schemas.study_schema import StudyRequest # 요청 데이터 형식을 정의한 Pydantic 모델
from services import agent_service 
from sqlalchemy.orm import Session #DB 연결 객체 타입(Session) 불러오기
from db.database import get_db #DB 연결 생성 함수 get_db 불러오기

from core.dependencies import get_current_user #JWT 인증 + 현재 사용자 확인 담당 파일)의 get_current_user 함수 불러오기

#===============================================================

router = APIRouter() # 라우터 객체 생성 (여기에 API들을 등록함)

@router.post("/agent") 
# 클라이언트가 POST 방식으로 "/agent" 경로로 요청을 보내면 아래 함수 실행

def run_agent(
    request: StudyRequest, #사용자 요청 데이터
    
    db: Session = Depends(get_db), 
    #get_db() 실행해서 DB연결 자동 준비
    #이제 학습 상태를 DB저장 해야해서 필요.
    
    current_user = Depends(get_current_user)
    #JWT 인증 실행 -> 현재 로그인 사용자 자동 조회
    # 내부적으로 벌어지는 일은 Authorization 헤더 확인 → JWT decode → user_id 추출 → DB에서 실제 사용자 조회 → current_user 반환
    # 즉 이제 current_user 안에는 실제 로그인 사용자 객체가 들어있다.(current_user.id , current_user.email)
    # 누가 요청했는지 알게 되는 첫 단계. 사용자별 학습 상태 저장이 가능해짐
    ):
  
    
    return agent_service.run(
        db=db, #현재 db연결 전달
        user_id=current_user.id, #jwt 인증으로 확인된 현재 로그인 사용자 id전달
        room_id=request.room_id,
        message=request.message, #사용자 입력 메시지 전달
        study_mode=request.study_mode #현재 학습 모드 전달
        )
        
    # request에서 message 값을 꺼내서 agent_service의 run 함수에 전달
    # → 실제 AI 처리(LLM 호출 등)는 service에서 수행됨
    # → 실행 결과를 그대로 클라이언트에게 응답으로 반환