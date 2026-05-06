# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from api import study_router  # ⭐ router import (경로 중요)
from api import agent_router



# FastAPI 앱 생성
app = FastAPI()

#router 연결
app.include_router(agent_router.router)

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

# router 연결 (핵심)
# 라우터 : 사용자의 요청을 받아서 어떤 기능으로 보낼지 결정하는 입구
app.include_router(study_router.router)



#로컬 서버 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)






#uvicorn main:app --reload