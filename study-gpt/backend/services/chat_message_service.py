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
     
    session = get_study_session(db,user_id,room_id) 
    message = ChatMessage(
        session_id=session.id if session else None, 
        room_id=room_id, 
        role=role,
        content=content 
        )
    
    #저장 후 새로고침, 반환
    db.add(message)
    
    #현재 room 조회
    room = db.query(StudyRoom).filter(
        StudyRoom.id == room_id
    ).first()
    
    #room 존재 시 updated_at 갱신
    if room:
        room.updated_at = datetime.utcnow() 
        
    db.commit()
    db.refresh(message)
    
    return message

# 2. 현재 로그인 사용자의 채팅방별 이전 대화 기록 전부 조회
def get_chat_messages(db: Session,room_id: int):

    messages = db.query(ChatMessage).filter(ChatMessage.room_id == room_id).order_by(asc(ChatMessage.id)).all()
    
    return messages