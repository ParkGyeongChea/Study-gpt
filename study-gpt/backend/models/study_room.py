#study_room.py

#room 테이블 구조 정의,
#user와 관계 연결

#쉽게 말하면 여러 개의 채팅창 목록을 만드는 것

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from sqlalchemy.orm import relationship # relationship 테이블끼리 관계를 연결하기 위해 가져오는 코드

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
    #ForeignKey = 테이블의 id와 연결한다는 뜻. 채팅방은 반드시 특정 사용자에게 속해야 함
    
    #채팅방 제목을 저장하는 코드
    title = Column(String)
    
    #채팅방이 만들어진 시간을 저장하는 코드
    created_at = Column(DateTime, default=datetime.utcnow)
    #DateTime = 날짜/시간 타입
    #default=datetime.utcnow = 새 채팅방이 만들어질 떄, 현재 시간을 자동으로 넣겠다는 뜻
    
    #채팅방이 마지막으로 수정된 시간을 저장하는 코드 , 최신 채팅이 제일 위로 오게
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    #default = 처음 생성될 떄 시간 저장
    #onupdate = 이 row 수정될 때마다 현재 시간 자동 갱신
    
    #이 채팅방과 사용자를 파이썬 코드에서 연결해주는 코드
    user = relationship("User", back_populates="study_rooms")
    # back_populates = 양쪽 모델을 서로 연결해주는 이름 연결 장치
    # study_rooms = relationship("StudyRoom", back_populates="user")은 user에서 연결.
    #쌍방향 연결이다. 채팅방과 유저는 연결되어야 함.
    #User 쪽 이름 = study_rooms
    # StudyRoom 쪽 이름 = user

    #chat_message 쪽과 쌍방향 연결
    messages = relationship("ChatMessage", back_populates="room")