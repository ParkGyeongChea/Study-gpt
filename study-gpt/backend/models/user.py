#models/user.py

#DB 연결 관리
#유저 테이블 

from sqlalchemy import Column, Integer, String
from db.database import Base
from sqlalchemy.orm import relationship

#1. 유저 DB 생성

class User(Base):

    __tablename__ = "users" 
    id = Column(Integer,primary_key=True,index=True) 
    
    #유저 이메일 컬럼 생성
    email = Column(String, unique=True, nullable=False)
    
    
    #패스워드 생성
    password = Column(String, nullable=False)
    
    #이 사용자가 가진 채팅방 목록을 연결하는 코드
    study_rooms = relationship(
        "StudyRoom",
        back_populates="user",
        cascade="all, delete-orphan"
        )

    
    #이 사용자의 학습 세션 목록 연결
    study_sessions = relationship(
        "StudySession",
        back_populates="user", 
        cascade="all, delete-orphan"
    )