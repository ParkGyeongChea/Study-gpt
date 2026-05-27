# session_service.py

# 사용자 학습 상태를 DB에 저장 / 조회 / 수정하는 서비스 파일

# ============================================================

from sqlalchemy.orm import Session
# SQLAlchemy DB 연결 객체 타입(Session) 불러오기

from models.study_session import StudySession
# models/study_session.py 파일(사용자 학습 상태 DB 테이블 역할)의
# StudySession 모델 클래스 불러오기


# ============================================================
# 학습 상태 저장 함수
# ============================================================

def save_study_session(
    db: Session,
    user_id: int,
    room_id: int,
    category,
    topic,
    level,
    curriculum,
    current_step_index,
    current_step,
    study_mode,
    learning_status
):

    # 현재 로그인 사용자의 기존 학습 기록 조회
    session = db.query(StudySession).filter(
        #db.query() = () 테이블 조회 시작 
        StudySession.user_id == user_id,
        StudySession.room_id == room_id
        #각 새로운 채팅방마다 새로운 session 시작
    ).first()

    # 기존 학습 기록이 있으면 UPDATE
    if session:

        session.category = category
        session.topic = topic
        session.level = level
        session.curriculum = curriculum
        session.current_step_index = current_step_index
        session.current_step = current_step
        session.study_mode = study_mode
        session.learning_status = learning_status

    # 기존 기록이 없으면 새로 생성 (INSERT)
    else:

        session = StudySession( 

            user_id=user_id,
            room_id=room_id,
            category=category,
            topic=topic,
            level=level,
            curriculum=curriculum,
            current_step_index=current_step_index,
            current_step=current_step,
            study_mode=study_mode,
            progress=0,
            learning_status=learning_status,
        )

        db.add(session)

    # 실제 DB 저장 확정
    db.commit()

    # 최신 DB 상태 다시 반영
    db.refresh(session)

    return session


# ============================================================
# 현재 학습 상태 조회 함수
# ============================================================

def get_study_session(
    db: Session,
    user_id: int,
    room_id: int
):

    session = db.query(StudySession).filter(
        StudySession.user_id == user_id,
        StudySession.room_id == room_id
        
    ).first()

    return session


# ============================================================
# 현재 학습 단계 index 수정 함수
# ============================================================

def update_step_index(
    db: Session,
    user_id: int,
    room_id: int,
    new_index
):

    session = db.query(StudySession).filter(
        StudySession.user_id == user_id,
        StudySession.room_id == room_id
    ).first()

    if session:

        session.current_step_index = new_index

        db.commit()

        db.refresh(session)

    return session


# ============================================================
# 현재 학습 step 객체 수정 함수
# ============================================================

def update_current_step(
    db: Session,
    user_id: int,
    room_id: int,
    step
):

    session = db.query(StudySession).filter(
        StudySession.user_id == user_id,
        StudySession.room_id == room_id
    ).first()

    if session:
        session.current_step = step
        db.commit()
        db.refresh(session)

    return session


# ============================================================
# 학습 모드 수정 함수
# ============================================================

def update_study_mode(
    db: Session,
    user_id: int,
    room_id: int,
    mode
):

    session = db.query(StudySession).filter(
        StudySession.user_id == user_id,
        StudySession.room_id == room_id
    ).first()

    if session:
        session.study_mode = mode
        db.commit()
        db.refresh(session)

    return session

# ============================================================
# 현재 학습 상태 수정 함수
# ============================================================

# 현재 사용자의 학습 상태를 DB에서 수정하는 역할
def update_learning_status(db: Session, user_id: int, room_id: int, learning_status: str):

    session = db.query(StudySession).filter(
        StudySession.user_id == user_id,
        StudySession.room_id == room_id
    ).first()

    if session:

        # 현재 학습 상태 수정
        session.learning_status = learning_status

        db.commit()
        db.refresh(session)

    return session