#chat_message.py


# 실제 사용자와 AI의 대화 내용을 저장하는 DB 테이블

from db.database import Base 
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    ForeignKey
)

#=====================================================

# 1.ChatMessage 클래스 생성
class ChatMessage(Base):
    __tablename__ = "chat_messages" #테이블 이름 지정
    
    #id 컬럼 생성 (pk=각 메시지의 고유 번호, index=True = 검색 속도 향상)
    id = Column(Integer, primary_key=True, index=True)
    
    #session_id 컬럼 생성
    session_id = Column(Integer,ForeignKey("study_sessions.id"),nullable=True) 
   
    #role 컬럼 (메시지 작성자 구분)
    role = Column(String)
    
    #contetn 컬럼
    content = Column(String) 
    
    #현재 메시지가 어느 room 소속인지 저장
    room_id = Column(Integer, ForeignKey("study_rooms.id"))
    
    # study_room과 relationship 추가.
    room = relationship("StudyRoom", back_populates="messages")