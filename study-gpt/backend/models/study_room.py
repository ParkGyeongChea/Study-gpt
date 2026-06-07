#study_room.py

#room 테이블 구조 정의,
#user와 관계 연결

#쉽게 말하면 여러 개의 채팅창 목록을 만드는 것

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship 
from datetime import datetime
from db.database import Base

#==============================

#.1 StudyRoom 모델 클래스 정의 , study_rooms 테이블 (채팅방 자체를 저장함)

class StudyRoom(Base):
    
    #테이블 이름
    __tablename__ = "study_rooms"
    
    #채팅방 고유 번호
    id = Column(Integer, primary_key=True, index=True)
    
    #이 채팅방이 어떤 사용자의 방인지 저장하는 코드.
    user_id = Column(Integer, ForeignKey("users.id"))
    
    #채팅방 제목을 저장하는 코드
    title = Column(String)
    
    # 부모 채팅방 id 저장 (하위 학습 구조용)
    parent_room_id = Column(
        Integer,
        ForeignKey("study_rooms.id"),
        nullable=True 
    )
    
    # 현재 진행 학습인지, 학습 아카이브인지 저장
    is_archived = Column(Boolean, default=False)
    
    #채팅방이 만들어진 시간을 저장하는 코드
    created_at = Column(DateTime, default=datetime.utcnow)
    
    #채팅방이 마지막으로 수정된 시간을 저장하는 코드 , 최신 채팅이 제일 위로 오게
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 유저 연결,이 채팅방과 사용자를 파이썬 코드에서 연결해주는 코드
    user = relationship(
        "User",
        back_populates="study_rooms"
        )
    
    #채팅 메시지 연결,chat_message 쪽과 쌍방향 연결
    messages = relationship(
        "ChatMessage",
        back_populates="room",
        cascade="all, delete-orphan"
    )
    
    # 현재 채팅방의 학습 세션 목록 연결
    sessions = relationship(
        "StudySession",
        back_populates="room",

        # 채팅방 삭제 시 세션도 삭제
        cascade="all, delete-orphan"
    )