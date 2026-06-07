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

from services import agent_service 
from sqlalchemy.orm import Session 
from db.database import get_db
from core.security import get_user_id_from_token 

#===============================================================

router = APIRouter()

@router.post("/agent") 

def run_agent(
    message: str = Form(...),
    study_mode: str = Form(...),
    room_id: int | None = Form(default=None),
    files: list[UploadFile] | None = File(default=None),
    db: Session = Depends(get_db), 
    authorization: str | None = Header(default=None)
    ):
    
    
    user_id = None
    
    # JWT 존재 시 로그인 사용자 조회
    if authorization: 
        
        try: 
            token = authorization.replace("Bearer ", "")
            user_id = get_user_id_from_token(token)
        except: 
            user_id = None
    
    return agent_service.run(
        db=db,
        user_id=user_id,
        room_id=room_id,
        message=message,
        study_mode=study_mode,
        files=files
        )
        
    # request에서 message 값을 꺼내서 agent_service의 run 함수에 전달
    # → 실제 AI 처리(LLM 호출 등)는 service에서 수행됨
    # → 실행 결과를 그대로 클라이언트에게 응답으로 반환