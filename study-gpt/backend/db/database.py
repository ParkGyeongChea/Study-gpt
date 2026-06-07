#database.py

#DB 연결 파일
#FastAPI <-> Superbase 연결 담당 파일

from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)


#실제 DB작업 공간 생성
SessionLocal = sessionmaker(
    autocommit=False, #자동 저장 금지
    autoflush=False, #자동 반영 금지
    bind=engine #이 session 은 engine(DB연결) 을 사용
)

#공통 부모 클래스(Base) 생성
Base = declarative_base()


#현재 모델들을 읽어서,Supabase DB에 실제 테이블 생성
Base.metadata.create_all(bind=engine)


#FastAPI 요청마다 DB작업 공간(Session)을 생성하고 관리하는 함수 생성
def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close() 