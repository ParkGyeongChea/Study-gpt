#chat_message_service.py

# 실제 사용자와 AI의 대화 내용을
# DB에 저장하는 서비스 파일

from services.session_service import get_study_session
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import asc
from models.chat_message import ChatMessage
from models.study_room import StudyRoom

#=================


# 1. 실제 메시지 저장 담당 함수 생성
def save_chat_message(
    db: Session,
    user_id: int,
    room_id: int,
    role: str,
    content: str
):
    
    #현재 로그인 사용자의 StudySession 조회
    
    session = get_study_session(db,user_id,room_id) 
    #chatmessage 는 어느 학습 세션의 메시지인지 알아야 함.
    # session_service.py 파일(DB 학습 상태 조회 역할)의 get_study_session 함수 호출
    # 현재 로그인 사용자의 # StudySession 데이터를 조회
    

    #chatmessage 객체 생성 (새 메시지 ORM 객체 생성)
    message = ChatMessage(
        session_id=session.id if session else None, 
        #삼항연산, 조건이 True 면 A False 면 B
        #session_id 이 존재하면 session.id 사용하고, 없으면 none 사용
        
        room_id=room_id, #어느 채팅방(room)인지 
        role=role, #메시지 작성자 역할
        content=content #실제 메시지 내용 저장
        )
    
    #저장 후 새로고침, 반환
    db.add(message)
    
    #현재 room 조회
    room = db.query(StudyRoom).filter(
        StudyRoom.id == room_id
    ).first()
    
    #room 존재 시 updated_at 갱신
    if room:
        room.updated_at = datetime.utcnow() #현재 시간으로 마지막 수정 시간 변경
        
    db.commit()
    db.refresh(message)
    
    return message

# 2. 현재 로그인 사용자의 채팅방별 이전 대화 기록 전부 조회
def get_chat_messages(db: Session,room_id: int):
    
    #ChatMessage 조회
    messages = db.query(ChatMessage).filter(ChatMessage.room_id == room_id).order_by(asc(ChatMessage.id)).all()
    #db.query(ChatMessage) =ChatMessage 테이블 조회 시작
    #.filter() = 현재 session_id 메시지만 조회 , 다른 사용자 대화 제외
    #.order_by(asc(ChatMessage.id)).all() = 오래된 메시지부터 정렬 후, 조회 결과 전부 리스트로 반환(.all)
    
    return messages