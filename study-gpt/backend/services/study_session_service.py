#study_session_service.py

#StudySession DB 저장/조회 전용 서비스 파일

from sqlalchemy.orm import Session
from models.study_session import StudySession


# 1. 저장 함수 생성 (사용자 학습 상태를 DB에 저장하는 함수)
def create_study_session(
    db: Session, #연결 객체
    user_id: int, #현재 로그인 사용자 번호
    topic: str, #현재 학습 주제
    level: str #현재 학습 난이도
):
    #StudySession 테이블 객체 생성
    new_session = StudySession(
        user_id=user_id,
        topic=topic,
        level=level
        #current_step/progress 안넣은 이유
        #models/study_session.py 에서, default 값을 default=1 default=0 으로 설정해둠.
        #자동으로 current_step = 1 progress = 0 으로 저장
    )
    #DB 저장
    db.add(new_session) #현재 생성한 학습 데이터를 DB저장 대상으로 등록
    
    #실제 db저장 확정
    db.commit()
    
    #db 새로고침 후 가져오기
    db.refresh(new_session)
    
    return new_session