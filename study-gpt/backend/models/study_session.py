#study_session.py

#사용자 학습 상태 DB 테이블 정의 , 사용자 공부 상태 저장 설계도

#================================================================================

from db.database import Base #모든 DB 테이블의 부모 클래스 역할을 하는 Base 불러오기
from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship

#================================================================================

# 1. StudySession DB 테이블 생성 클래스
class StudySession(Base):
    __tablename__ = "study_sessions" 
    
    id = Column(Integer, primary_key=True, index=True)
    #숫자 타입 / 기본키(각 데이터 고유 번호) / 검색 속도 향상
    
    #현재 study_session 데이터가 어느 사용자 것인지 연결
    user_id = Column(
        Integer,
        ForeignKey("users.id")
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
    
    # 현재 학습 상태 저장 컬럼
    learning_status = Column(String, default="learning")
    
    #Level 컬럼 ,난이도 저장 컬럼
    level = Column(String)
    
    #현재 퀴즈의 정답 데이터 저장
    quiz_answer_data = Column(JSON, nullable=True)
    
    #current_step 컬럼 (몇 단계 공부 중인지 저장하는 데이터 default=1 은 기본적으로 1단계부터 시작)
    current_step = Column(JSON)
    
    #current_step_index (현재 몇 번 째 단계인가)
    current_step_index = Column(Integer, default=0)
    
    #progress 컬럼 (현재 학습 진행률 저장 컬럼 Interger= 퍼센트 숫자로 저장. / 기본적으로 0%시작)
    progress = Column(Integer, default=0)
    
        
    # User 모델과 연결 
   
    user = relationship(
        "User",
        back_populates="study_sessions"
    )

    
    # StudyRoom 모델과 연결
    
    room = relationship(     
        "StudyRoom",
        back_populates="sessions"
    )