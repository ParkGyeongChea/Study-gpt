#user.py

#DB 연결 관리
#유저 테이블 

from sqlalchemy import Column, Integer, String
from db.database import Base
from sqlalchemy.orm import relationship

#1. 유저 DB 생성

class User(Base): #user 라는 db 모델 클래스 생성

    __tablename__ = "users" 
    #실제 PostgreSQL 안에서 생성될 테이블 이름을 정하는 코드.
    #왜 Users?  DB에서는 복수형을 많이 사용 .
    
    #유저 ID 생성
    id = Column(Integer,primary_key=True,index=True) 
    #유저 고유 번호(id) 컬럼 생성
    #Interger = 숫자 데이터, primary_key=Treu = 이 컬럼을 테이블 대표 번호(절대 중복되지 않는 고유 번호)로 사용 ,
    #index=True = 검색 속도 향상 기능 사용
    
    #유저 이메일 컬럼 생성
    email = Column(String, unique=True, nullable=False)
    #문자열, unique = 중복 금지 , nullable = 반드시 입력해야 함
    
    #패스워드 생성
    password = Column(String, nullable=False)
    #일반 평문 비밀번호 저장 금지 설정
    #반드시 나중에 bcrypt 해시 암호화 해서 저장해야 함
    
    
    #이 사용자가 가진 채팅방 목록을 연결하는 코드
    study_rooms = relationship("StudyRoom", back_populates="user")
    # back_populates = 양쪽 모델을 서로 연결해주는 이름 연결 장치
    #user = relationship("User", back_populates="study_rooms") 은 study_room에서 연결.
    #쌍방향 연결이다. 채팅방과 유저는 연결되어야 함.
    #User 쪽 이름 = study_rooms
    # StudyRoom 쪽 이름 = user