# llm_service.py


import json
from services.shared_llm import llm 
from services.chains.curriculum_chain import curriculum_chain
from services.chains.analyze_chain import analyze_chain
from services.chains.intent_chain import intent_chain
from dotenv import load_dotenv
load_dotenv()



# 1. 커리큘럼 생성 함수 , 문장형 커리큘럼 리스트 반환 , 커리큘럼의 품질 담당
def generate_curriculum(category: str, topic: str, level: str, step_count: int):
   
    response = curriculum_chain.invoke({
        "category": category,
        "topic": topic,
        "level": level,
        "step_count": step_count
    })

    try: #파싱 성공 시, GPT 결과를 사용한다.
        curriculum = json.loads(response.content.strip()) 

        if not isinstance(curriculum, list): 
            raise ValueError("커리큘럼 결과가 리스트가 아닙니다.")

        return curriculum[:step_count] 
         
    except: 
        return [
            f"{category}의 핵심 개념을 초보자 눈높이에서 이해하기",
            f"{topic}과 관련된 기본 용어와 흐름 익히기",
            f"{topic}의 주요 개념을 예시와 함께 학습하기",
            f"{topic}을 간단한 문제나 실습으로 적용해보기",
            f"{category} 학습을 계속 이어가기 위한 다음 단계 정리하기"
        ][:step_count]
        
        
# 2. 과목, 레벨 추출 함수
def analyze_user_input(message: str): 
    
    response = analyze_chain.invoke({
        "message": message
    })
        
    try:
        result = json.loads(response.content.strip())
       
    except: 
        return "일반", "초급", "기초" 
    
    category = result.get("category", "일반") 
    level = result.get("level", "초급")
    topic = result.get("topic", "기초")   
    bad_topics = ["공부", "공부하기", "학습", "배우기", "일반"]

    
    if len(topic.strip()) < 2 or topic.strip() in bad_topics: 
   
        topic = "기초"

    return category, level, topic

    
    

if __name__ == "__main__":
    print(analyze_user_input("파이썬 중급 배우고 싶어"))
    print(analyze_user_input("파이썬 처음 배우고 싶어"))
    print(analyze_user_input("백엔드 API 제대로 배우고 싶어"))
    print(analyze_user_input("영어 회화 중급 수준으로 공부하고 싶어"))
    


# 3. Intent 분석 함수 
# 어떤 기능(설명,퀴즈..등..)을 실행할지 결정하는 함수
def analyze_intent(message: str):
    response = intent_chain.invoke({
        "message": message
    }) 
    
    try:
        result = json.loads(response.content.strip())
        
    except:
        return "chat"
    
    intent = result.get("intent", "chat") 
    intent = intent.lower() 
    intent = intent.strip() 
    
    # GPT가 전혀 다른 값을 줄떄 , chat으로 흘려보내는 코드
    valid_intents = ["study", "explain", "quiz", "chat"] 
    
    if intent not in valid_intents: 
        intent = "chat"
        

    return intent