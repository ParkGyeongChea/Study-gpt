#study_session.py

#사용자 학습 상태 DB 테이블 정의 , 사용자 공부 상태 저장 설계도

#================================================================================

from db.database import Base #모든 DB 테이블의 부모 클래스 역할을 하는 Base 불러오기
from sqlalchemy import Column, Integer, String, ForeignKey, JSON

# sqlalchemy 공간(DB ORM 기능 모음)의
# Column = 테이블 컬럼 생성 기능
# Integer = 숫자 타입
# String = 문자 타입
# ForeignKey = 다른 테이블 연결 기능 불러오기
# (study_session 은 어떤 사용자의 공부 데이터인지 알아야 함. 그래서 user테이블과 연결해야 하는데 그 기능을 하는 것 ForeignKey)
# JSON 사용 이유 = curriculum 은 python 구조체 데이터라 일반 string저장이 맞지 않다

#================================================================================

# 1. StudySession DB 테이블 생성 클래스
class StudySession(Base):
    __tablename__ = "study_sessions" #테이블명 설정
    
    id = Column(Integer, primary_key=True, index=True)
    #숫자 타입 / 기본키(각 데이터 고유 번호) / 검색 속도 향상
    
    #현재 study_session 데이터가 어느 사용자 것인지 연결
    user_id = Column(
        Integer,
        ForeignKey("users.id") #user테이블의 id와 연결
    )
    
    #현재 room 소속 조회
    room_id = Column(
        Integer,
        ForeignKey("study_rooms.id")
    )
    
    # StudySession 테이블 구조 설계
    
    #현재 학습 주제 저장 컬럼
    topic = Column(String)
    
    #catrgory 컬럼 추가
    category = Column(String)
    
    #curriculum 컬럼 추가(전체 커리큘럼 저장)
    curriculum = Column(JSON)
    
    #Study_mode 컬럼 추가 (현재 학습 모드 저장)
    study_mode = Column(String)
    
    #Level 컬럼 ,난이도 저장 컬럼
    level = Column(String)
    
    #current_step 컬럼 (몇 단계 공부 중인지 저장하는 데이터 default=1 은 기본적으로 1단계부터 시작)
    current_step = Column(JSON)
    
    #current_step_index (현재 몇 번 째 단계인가)
    current_step_index = Column(Integer, default=0)
    
    #progress 컬럼 (현재 학습 진행률 저장 컬럼 Interger= 퍼센트 숫자로 저장. / 기본적으로 0%시작)
    progress = Column(Integer, default=0)