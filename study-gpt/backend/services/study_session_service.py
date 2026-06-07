#study_session_service.py

#StudySession DB 저장/조회 전용 서비스 파일

from sqlalchemy.orm import Session
from models.study_session import StudySession


# 1. 저장 함수 생성 (사용자 학습 상태를 DB에 저장하는 함수)
def create_study_session(
    db: Session, 
    user_id: int, 
    topic: str, 
    level: str 
):
    #StudySession 테이블 객체 생성
    new_session = StudySession(
        user_id=user_id,
        topic=topic,
        level=level   
    )
    
    db.add(new_session) 
    db.commit()
    db.refresh(new_session)
    
    return new_session