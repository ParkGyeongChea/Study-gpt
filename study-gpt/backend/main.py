# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from api import study_router  #  router import (경로 중요)
from api import agent_router
from api import side_chat_router
from api import study_room_router

#DB 관련 import
from db.database import engine, Base #만들어둔 DB 연결(engine) , SQLAQLAlchemy 부모(Base) 가져옴
from models.user import User # SQLAlchemy는 import된 모델만 인식. 하지 않으면 User테이블 존재 자체를 모름
from models.study_session import StudySession
from api.user_router import router as user_router
#as user_router =  충돌 방지를 위해 api.user_router 안의 router를 user_router 라는 이름으로 사용

from models.study_room import StudyRoom
#studyroom 클래스 메모리에 등록시키기 위해 사용.비활성화 처럼 보여도 정상 등록 목적 import다


# FastAPI 앱 생성
app = FastAPI()

#에러 디버깅 코드 ============
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#=========

#Base에 등록된 모든 테이블 실제 DB에 생성
Base.metadata.create_all(bind=engine)
#metadata = 등록된 테이블 정보 목록
#creatre_all 실행 시 users 테이블 생성 SQL 자동 실행.
#bind=engine = 어떤 DB 연결 사용할지 지정 (Supabase PostgreSQL 에 생성해라)



#router 연결
# 라우터 : 사용자의 요청을 받아서 어떤 기능으로 보낼지 결정하는 입구
app.include_router(agent_router.router)
app.include_router(side_chat_router.router)
app.include_router(study_router.router)
app.include_router(user_router) #회원가입 api를 FastAPI 서버에 등록
app.include_router(study_room_router.router)

#환경변수 로드
load_dotenv()

#CROS 설정 (React 연결)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#로컬 서버 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)



#uvicorn main:app --reload