# agent_service.py

#역할
#message 입력-> intent 분석 -> 기능 분기 -> 결과 반환

from services.llm_service import analyze_intent
from services.curriculum_service import start_study_service
from services.explain_service import explain_service


def run(message: str): #router 에서 이 함수를 호출함. 반드시 필요
    intent = analyze_intent(message) #이 함수에서 제일 먼저 해야 할 일. intent 분석
    print("intent:", intent)
    
    if intent == "study":
        return start_study_service(message)  #메세지 리턴
    
    #explain 임시 응답
    
    elif intent == "explain":
        return explain_service(message)
    
    
    #quiz 임시 응답
    elif intent == "quiz":
        return {"message": "퀴즈 기능 준비중"}
    
    else:
        return {"message": "일반 대화 기능 준비중"}
    
