#chat_message.py


# 실제 사용자와 AI의 대화 내용을 저장하는 DB 테이블

from db.database import Base #DB테이블 Base 상속을 받아야 이 클래스는 db테이블이다 라고 인식함
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column, #db컬럼 생성
    Integer, #숫자
    String, #문자열
    ForeignKey #다른 테이블 연결 기능
)

#=====================================================

# 1.ChatMessage 클래스 생성
class ChatMessage(Base):
    __tablename__ = "chat_messages" #테이블 이름 지정
    
    #id 컬럼 생성 (pk=각 메시지의 고유 번호, index=True = 검색 속도 향상)
    id = Column(Integer, primary_key=True, index=True)
    
    #session_id 컬럼 생성
    session_id = Column(Integer,ForeignKey("study_sessions.id")) 
    # 현재 메시지가 어느 StudySession(학습 세션)의 대화인지 연결
    # study_sessions 테이블의 id와 연결된다.
    
    
    #role 컬럼 (메시지 작성자 구분)
    role = Column(String) #프론트에서 , user메시지는 오른쪽, ai메시지는 왼쪽 같은 UI 를 만들수 있음
    
    #contetn 컬럼
    content = Column(String) #실제 메시지 저장
    
    #현재 메시지가 어느 room 소속인지 저장
    room_id = Column(Integer, ForeignKey("study_rooms.id"))
    
    # study_room과 relationship 추가.
    room = relationship("StudyRoom", back_populates="messages")