#study_router.py

#사용자가 보낸 요청을 처음 받는 파일. service 호출만 함.

from fastapi import APIRouter #FastAPI 에서 API를 만들려면 라우터 객체가 있어야 한다.
from services.curriculum_service import start_study_service #servicer 파일에서 함수 가져오기
from pydantic import BaseModel #Pydantic 객체 = "데이터를 검증하고 정리해주는 Python 객체" / 사용자 입력을 안전하게 받기 위한 틀
from typing import List

router = APIRouter() #라우터 객체를 만들었기 때문에, 이 파일에서 사용할 라우터를 만듬

class StudyRequest(BaseModel): #사용자가 보내는 데이터 형식 정의. / 입력 데이터 구조 만들기
    message: str               #"message" 라는 이름의 문자열만 받음

class StudyResponse(BaseModel):#서버가 사용자에게 돌려줄 데이터 구조 / 응답 데이터 구조 만들기
    
    #사용하는 이유
    #데이터 자동 검증, 틀린 데이터 못 나가게 막음
    #Swagger 문서 자동 생성 < 여기서 결과 구조 자동으로 보여줌.
    #프론트 개발시 필수(프론트가 어떤 데이터 오는지 정확히 할 수 있음.)
    
    category: str #카테고리: 문자열
    curriculum: List[str] #커리큘럼: 문자열 리스트
                            # list[str] = Python 3.9+
                            # List[str] = 더 표준적인 타입 힌트 (FastAPI에서 안정적)

@router.post("/study/start", response_model=StudyResponse) 
# 사용자의 학습 요청을 받아 커리큘럼을 생성하는 API
# POST 요청으로 전달된 데이터를 처리한 후, 결과를 StudyResponse 형식으로 반환

       
def start_study(request: StudyRequest):

    message = request.message
    # 현재 (FastAPI 객체 방식)
    # request가 객체(object) 일때 사용.데이터 구조가 바뀌었기 떄문에 접근/꺼내는 방식이 바뀜.
    
    result = start_study_service(message) #꺼낸 message를 service로 넘김. (이제 service는 request 문자열 하나만 받으면 됨)
    return result #service 결과를 그대로 사용자에게 돌려준다.
    
    # return StudyResponse(**result)
    # 타입 검증 한번 더. 응답 구조 강제
    
    # if "error" in result:
    #     return result  # 또는 HTTPException
