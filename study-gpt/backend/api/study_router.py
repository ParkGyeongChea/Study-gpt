#study_router.py

#사용자가 보낸 요청을 처음 받는 파일. service 호출만 함.

from fastapi import APIRouter #FastAPI 에서 API를 만들려면 라우터 객체가 있어야 한다.
from services.curriculum_service import start_study_service #servicer 파일에서 함수 가져오기 

router = APIRouter() #라우터 객체를 만들었기 때문에, 이 파일에서 사용할 라우터를 만듬


@router.post("/study/start") #API 만들기.데이터를 서버로 보냄 -> POST. POST로 /study/start 요청 오면 아래 함수를 실행.

       
def start_study(request:dict): #사용자가 보낸 json 데이터를 request로 받는다.           
    message = request["message"] #사용자가 보낸 데이터 중에서, 핵심 데이터인 message만 꺼냄
    result = start_study_service(message) #꺼낸 message를 service로 넘김. (이제 service는 request 문자열 하나만 받으면 됨)
    return result #service 결과를 그대로 사용자에게 돌려준다.
   
