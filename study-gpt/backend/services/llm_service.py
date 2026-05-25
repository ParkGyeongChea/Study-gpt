# llm_service.py


import json
from services.shared_llm import llm #공용 GPT 객체 사용
from services.chains.curriculum_chain import curriculum_chain
from services.chains.analyze_chain import analyze_chain
from services.chains.intent_chain import intent_chain
from dotenv import load_dotenv
load_dotenv()




# 1. 커리큘럼 생성 함수 , 문장형 커리큘럼 리스트 반환 , 커리큘럼의 품질 담당
def generate_curriculum(category: str, topic: str, level: str, step_count: int):
    # category, topic, level, step_count 값을 받아서 LLM에게 넘긴다.

    response = curriculum_chain.invoke({
        "category": category,
        "topic": topic,
        "level": level,
        "step_count": step_count
    })

    try: #파싱 성공 시, GPT 결과를 사용한다.
        curriculum = json.loads(response.content.strip()) #gpt가 보낸 문자열을 python 리스트로 바꿈

        if not isinstance(curriculum, list): #isinstance = "이 값이 특정 타입(형식)이 맞는지 확인하는 함수"
            raise ValueError("커리큘럼 결과가 리스트가 아닙니다.")

        return curriculum[:step_count] 
        #커리큘럼 반환
        # :step_count 는 혹시 GPT가 많이 생성했을 때 필요한 개수만 자르는 코드 

    except: #json 파싱 실패, 리스트 형식 오류 등 문제 시, 아래의 기본값 사용.
        return [
            f"{category}의 핵심 개념을 초보자 눈높이에서 이해하기",
            f"{topic}과 관련된 기본 용어와 흐름 익히기",
            f"{topic}의 주요 개념을 예시와 함께 학습하기",
            f"{topic}을 간단한 문제나 실습으로 적용해보기",
            f"{category} 학습을 계속 이어가기 위한 다음 단계 정리하기"
        ][:step_count]
        
        #llm 응답이 깨졌을때 사용하는 안전장치.
        #서비스가 멈추지 않고 기본 커리큘럼이라도 반환하게 만듬


# 2. 과목, 레벨 추출 함수
def analyze_user_input(message: str): #사용자 입력-> 과목-> 레벨 추출 함수 추가
    
    #analyze_chain 의 {message}변수 안에 "message": message 형태로 실제 값을 넣어줌
    response = analyze_chain.invoke({
        "message": message
    })
        
    try:
        result = json.loads(response.content.strip())
        # response.content는 GPT가 응답한 실제 내용
        # json.loads = 문자열을 파이썬 딕셔너리로 변경
              
    except: #에러처리 . JSON 형식이 아니라 다른 방식으로 답하면,
        return "일반", "초급", "기초" # JSON 변환에 실패했을 떄 기본값을 반환
    
    category = result.get("category", "일반") #category가 있으면 가져오고, 없으면 “일반”을 기본값으로 사용한다.
    level = result.get("level", "초급")
    topic = result.get("topic", "기초")
    
    # topic 품질 보정
    # GPT가 topic을 "공부", "공부하기", "학습"처럼 너무 애매하게 줄 경우
    # 커리큘럼 생성 기준으로 사용하기 어렵기 때문에 기본값인 "기초"로 보정한다.
    
    bad_topics = ["공부", "공부하기", "학습", "배우기", "일반"]

    
    if len(topic.strip()) < 2 or topic.strip() in bad_topics: 
        #topic을 검사해서 너무 짧거나, bad_topics 안에 들어있으면 아래 코드를 실행해라.
        
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
    #intent_chain 의 {message}변수 안에 "message": message 형태로 실제 값을 넣어줌
    response = intent_chain.invoke({
        "message": message
    }) 
    
    try:
        result = json.loads(response.content.strip())
        
    except:
        return "chat"
    #실패했는데 study로 보내면 사용자가 질문을 했는데 커리큘럼이 생성될수 있음.
    #그래서 실패시, 안전한 값인 일반 대화 chat 으로 보냄
    
    intent = result.get("intent", "chat") #GPT가 준 값 가져오기, 없으면 chat으로 안전 처리
    intent = intent.lower() #lower = gpt 는 대문자로도 값을 반환할수 있음. 그래서 소문자로 처리하는 함수
    intent = intent.strip() 
    
    #=== GPT가 전혀 다른 값을 줄떄 , chat으로 흘려보내는 코드 ===
    
    valid_intents = ["study", "explain", "quiz", "chat"] #반환 시 정답 목록
    
    #gpt가 이상하게 응답했을떄 ex)result = {"intent": "studyy"}
    # agent_servicer에서, if intetnt == "study": 니까, 값이 들어가지 않는다.
    # 그래서, "일반 대화 기능 준비중" 이라는 맞지 않는 결과가 나옴.
    # 이상한 값이면 , chat으로 보내버려야 함.

    if intent not in valid_intents: #intent 값이 우리가 허용한 목록에 없으면,
        intent = "chat"
        

    return intent