#database.py

#DB 연결 파일
#FastAPI <-> Superbase 연결 담당 파일

from sqlalchemy import create_engine 
#파이썬으로 DB를 쉽게 다루게 해주는 도구
#create_engine = DB연결 기재(엔진) 만들기

from sqlalchemy.orm import sessionmaker
#DB 작업용 연결(Session=DB랑 대화하는 작업 공간) 만드는 도구 

from sqlalchemy.orm import declarative_base
#이 코드는 User, StudySession , CurriculumStep , Progress 같은 모든 DB 테이블들의 공통 부모 클래스를 만드는 코드.
#declarative_base() = DB테이블들의 부모 클래스 생성

from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
#중요, FastAPI <-> Superbase 연결 생성을 실제로 수행.
#DATABASE_URL = DB 주소 , create_engine = 그 주소로 실제 연결 통로 생성 수
#engine = DB연결 관리자
#이 줄이 실행되면, SQLAlchemy가, PostgreSQL 종류 확인, psycopg2 사용, Supabase 서버 연결 준비 를 자동으로 처리한다.

#SQLAlchemy 는 DATABASE_URL 안의 (.env의 superbase url) postgresql+psycopg2://postgres:Rudco%400214%23$@db~~~ 
# 이 부분을 보고 PostgreSQL 연결이라고 판단.
#PostgreSQL 은 DB 종류를 말함 (SQLite,MySQL,MariaDB,MongoDB...)
#psycopg2 = PostgreSQL 전용 연결 드라이버
#Python은 원래 PostgreSQL 언어를 못 알아듣는다. 연결 드라이버.


#실제 DB작업 공간 생성
SessionLocal = sessionmaker(
    autocommit=False, #자동 저장 금지
    autoflush=False, #자동 반영 금지
    bind=engine #이 session 은 engine(DB연결) 을 사용
)

#공통 부모 클래스(Base) 생성
Base = declarative_base()
#class User(Base): = "User 라는 DB 테이블 만들겠다"

# 그런데 왜 Base 가 필요?
# Python은 원래 이 클래스가 일반 클래스인지 DB 테이블용 클래스인지 모른다.
# 그래서 SQLAlchemy에게 알려줘야 한다
# "이 클래스는 DB 테이블용이다". 그 역할을 하는게 Base


#FastAPI 요청마다 DB작업 공간(Session)을 생성하고 관리하는 함수 생성
def get_db():
    db = SessionLocal() #db 작업 공간 생성
    try:
        yield db #이 db 연결을 API에서 사용하라는 뜻
    finally: #에러가 나더라도 무조건 연결 종료하게 만들기 위해서.
        db.close() #작업 끝나면 DB연결 종료