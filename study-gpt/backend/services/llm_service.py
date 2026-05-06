# llm_service.py
# GPT 호출
# GPT에게 커리큘럼 생성 요청

import json
from langchain_openai import ChatOpenAI
# from langchain_core.prompts import ChatPromptTemplate #대화
# from langchain_core.output_parsers import StrOutputParser #문자 형태로 출력
from dotenv import load_dotenv
load_dotenv()


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7
    )

# 1. 커리큘럼 생성 함수 , 문장형 커리큘럼 리스트 반환 , 커리큘럼의 품질 담당

def generate_curriculum(category: str, topic: str, level: str, step_count: int):
    # category, topic, level, step_count 값을 받아서 LLM에게 넘긴다.
    prompt = f"""
        너는 초보자를 위한 학습 커리큘럼을 설계하는 AI 튜터다.

        [입력 정보]
        - 과목: {category}
        - 학습 주제: {topic}
        - 학습 수준: {level}
        - 단계 수: {step_count}

        ----------------------------------------

        [목표]
        사용자가 실제로 공부를 시작할 수 있도록,
        {step_count}단계의 학습 커리큘럼을 만들어라.

        각 단계는 단순한 단어가 아니라,
        "무엇을 배우는지"가 분명한 문장으로 작성하라.

        ----------------------------------------

        [중요 규칙]

        1. 절대 아래처럼 출력하지 마라:
        - "{topic} 학습을 위한 단계 1"
        - "{topic} 학습을 위한 단계 2"
        - "1단계"
        - "기초 학습"
        - "개념 이해"

        2. 각 단계는 반드시 실제 학습 내용이어야 한다.

        3. 사용자가 "기초", "기본", "처음", "입문"을 요청한 경우:
        - 해당 과목의 전체 기초 흐름을 단계별로 구성하라.
        - 특정 개념 하나에만 치우치지 마라.

        4. 사용자가 특정 개념을 요청한 경우:
        - 해당 개념을 중심으로 단계별 설명 흐름을 구성하라.

        5. {level} 수준에 맞게 난이도를 조절하라.

        ----------------------------------------

        [좋은 예시]

        입력:
        - 과목: 파이썬
        - 학습 주제: 파이썬 기초 전체
        - 학습 수준: 초급
        - 단계 수: 5

        출력:
        [
        "파이썬이 무엇이고 어떤 분야에서 사용되는지 이해하기",
        "변수와 데이터 타입을 사용해 값을 저장하는 방법 배우기",
        "조건문을 사용해 상황에 따라 코드를 다르게 실행하는 방법 익히기",
        "반복문을 사용해 같은 작업을 여러 번 처리하는 방법 배우기",
        "함수를 만들어 코드를 재사용하는 기본 방법 익히기"
        ]

        ----------------------------------------

        [출력 규칙]
        - 반드시 JSON 배열만 출력하라.
        - 설명 문장 금지
        - 코드블록 금지
        - 번호를 문자열 안에 넣지 마라.
        - 배열의 길이는 반드시 {step_count}개여야 한다.

        출력 형식:
        [
        "첫 번째 학습 단계",
        "두 번째 학습 단계",
        "세 번째 학습 단계"
        ]
        """

    response = llm.invoke(prompt) #위의 프롬프트를 실제 llm에게 보냄.

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
    prompt = f"""
        너는 사용자의 학습 요청을 분석하여 구조화된 데이터로 변환하는 AI다.

        [입력]
        "{message}"

        ----------------------------------------

        [목표]
        사용자의 입력을 분석하여 아래 3가지 정보를 추출하라:

        1. category (과목 이름)
        - 사용자가 배우고자 하는 분야를 그대로 반영
        - 제한 없이 자유롭게 생성
        - 예: "파이썬", "영상 편집", "플로리스트", "게임 개발"

        2. topic (세부 학습 주제)
        - 해당 과목에서 실제로 배우는 "구체적인 학습 대상"이어야 한다
        - 반드시 명확한 개념, 기술, 작업 단위로 작성

        매우 중요:
        - 절대 추상적인 표현을 사용하지 마라

        금지 표현:
        - "공부"
        - "학습"
        - "이해하기"

        ----------------------------------------

        예외 규칙 (핵심 추가)

        - 사용자가 아래와 같은 표현을 포함하면:
        "기본", "기초", "처음", "입문", "시작"

        → 특정 개념 하나가 아니라  
        → 해당 과목의 전체 기초 학습 흐름을 대표하는 topic을 생성하라

        예:
        - "파이썬 기본 배우고 싶어" → "파이썬 기초 전체"
        - "영상편집 처음 배우고 싶어" → "영상 편집 입문 전체 흐름"

        ----------------------------------------

        예시 변환:

        - "플로리스트 배우고 싶어" → "꽃다발 제작"
        - "한문 기초 배우고 싶어" → "기초 한자 학습 흐름"
        - "랭체인 배우고 싶어" → "체인 구조 설계"

        ----------------------------------------

        3. level (학습 수준)
        - 반드시 다음 중 하나만 선택:
        "초급", "중급", "고급"

        ----------------------------------------

        [level 판단 기준]
        - 초급: 입문, 처음, 기초, 초보
        - 중급: 경험 있음, 중간 수준
        - 고급: 심화, 전문가

        ----------------------------------------

        [출력 규칙]
        - 반드시 JSON 한 줄만 출력
        - JSON 외 텍스트 절대 금지
        - 설명 금지
        - 코드블록 금지

        ----------------------------------------

        [출력 형식]
        {{"category": "파이썬", "topic": "파이썬 기초 전체", "level": "초급"}}
        """
    
    response = llm.invoke(prompt)
    
    
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
    prompt = f"""
        너는 사용자의 메시지를 분석하여 "의도(Intent)"를 분류하는 AI다.

        [입력]
        "{message}"

        ----------------------------------------

        [Intent 종류]

        1. study
        - 학습을 시작하거나, 무엇을 어떻게 배워야 하는지 묻는 경우

        2. explain
        - 특정 개념, 기술, 도구 하나를 설명해달라는 경우

        3. quiz
        - 문제를 요청하는 경우

        4. chat
        - 일반 대화

        ----------------------------------------

        [핵심 판단 기준 ]

        다음 기준을 반드시 따르라:

        ----------------------------------------

        1. "학습 시작" 의도가 있으면 → study

        다음 표현이 포함되면 study로 판단하라:

        - 배우고 싶어
        - 공부하고 싶어
        - 기초부터
        - 어떻게 시작
        - 어떤 순서
        - 커리큘럼
        - 과정

         이 경우,
        "설명해줘"가 함께 있어도 study로 판단하라

        ----------------------------------------

        2. "단일 개념 설명"이면 → explain

        다음 경우 explain:

        - 특정 개념 하나만 설명 요청
        - 학습 흐름 없이 설명만 요구

        예:
        - "파이썬 함수 설명해줘"
        - "DLSS 기능 뭐야"

        ----------------------------------------

        3. quiz

        - 문제 내줘, 퀴즈 요청

        ----------------------------------------

        4. 나머지 → chat

        ----------------------------------------

        [출력 규칙]

        - 반드시 JSON 한 줄만 출력
        - JSON 외 텍스트 절대 금지

        ----------------------------------------

        [출력 형식]

        {{"intent": "study"}}
        """
    
    response = llm.invoke(prompt) #GPT 호출
    
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
        
    #===================
    

    return intent