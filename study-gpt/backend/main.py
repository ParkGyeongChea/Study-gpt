# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
load_dotenv(override=True)

from api import study_router  
from api import agent_router
from api import side_chat_router
from api import study_room_router
from db.database import engine, Base
from models.user import User 
from models.study_session import StudySession
from api.user_router import router as user_router
from models.study_room import StudyRoom


app = FastAPI()

#에러 디버깅 코드 
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://study-gpt-one.vercel.app",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

#router 연결
app.include_router(agent_router.router)
app.include_router(side_chat_router.router)
app.include_router(study_router.router)
app.include_router(user_router) 
app.include_router(study_room_router.router)



# #CROS 설정 (React 연결)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


#로컬 서버 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)



#uvicorn main:app --reload