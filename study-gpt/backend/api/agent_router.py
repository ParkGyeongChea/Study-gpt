#agent_router.py

# 사용자 요청을 받아서 → agent_service로 전달하는 역할 (라우터 = API 입구)

from fastapi import (
    APIRouter,
    Depends,
    Header,
    UploadFile,
    File,
    Form
)
#Depends= 필요한 기능 자동 실행 기능 , Header = JWT 토큰 없어도 허용하는 수동 처리
from services import agent_service 
from sqlalchemy.orm import Session #DB 연결 객체 타입(Session) 불러오기
from db.database import get_db #DB 연결 생성 함수 get_db 불러오기

from core.security import get_user_id_from_token #JWT-> user_id 추출을 직접 시도하려고 가져옴

#===============================================================

router = APIRouter() # 라우터 객체 생성 (여기에 API들을 등록함)

@router.post("/agent") 
# 클라이언트가 POST 방식으로 "/agent" 경로로 요청을 보내면 아래 함수 실행

def run_agent(
    message: str = Form(...),
    study_mode: str = Form(...),
    room_id: int | None = Form(default=None),
    files: list[UploadFile] | None = File(default=None),
    
    db: Session = Depends(get_db), 
    #get_db() 실행해서 DB연결 자동 준비
    #이제 학습 상태를 DB저장 해야해서 필요.
    
    authorization: str | None = Header(default=None)
    #str | None = 문자열 또는 none 허용
    #브라우저가 보내는 JWT 토큰 문자열 저장 변수, HTTP 헤더에서 값을 가져옴
    #default=None = JWT 없어도 에러가 나지 않음
    
    ):
    
    # 기본값은 비로그인 사용자
    user_id = None
    
    # JWT 존재 시 로그인 사용자 조회
    if authorization: #JWT 토큰이 존재하나? 검사
        
        try: #여기서 JWT 해석 시도
            
            # "Bearer xxx" 에서 JWT만 추출
            token = authorization.replace("Bearer ", "")

            # JWT에서 user_id 추출
            user_id = get_user_id_from_token(token)
            
        #JWT 만료/오류 발생 시 로그인 실패 처리
        except: 
            user_id = None
    
    return agent_service.run(
        db=db, #현재 db연결 전달
        user_id=user_id,
        room_id=room_id,
        message=message, #사용자 입력 메시지 전달
        study_mode=study_mode, #현재 학습 모드 전달
        files=files
        )
        
    # request에서 message 값을 꺼내서 agent_service의 run 함수에 전달
    # → 실제 AI 처리(LLM 호출 등)는 service에서 수행됨
    # → 실행 결과를 그대로 클라이언트에게 응답으로 반환