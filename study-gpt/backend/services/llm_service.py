#llm_service.py
#GPT 호출
import json
from langchain_openai import ChatOpenAI
# from langchain_core.prompts import ChatPromptTemplate #대화
# from langchain_core.output_parsers import StrOutputParser #문자 형태로 출력
from dotenv import load_dotenv
load_dotenv()


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.5
    )


def generate_curriculum(category: str, topic: str, level: str, step_count: int): #이 함수는 과목 이름 하나를 받음.
    
    #GPT 지시문 , {category} 넣어 과목 바꿀수 있게 하고 JSON형식 강제
    prompt = f"""
    너는 어떤 분야든 학습 커리큘럼을 설계하는 전문가다.

    [입력]
    과목: {category}
    세부 주제: {topic}
    학습 수준: {level}

    ----------------------------------------

    [핵심 규칙]
    - 반드시 "{topic}" 중심으로 커리큘럼을 구성하라
    - 해당 분야에서 실제로 배우는 내용만 포함하라
    - 모든 분야(기술, 예술, 언어, 자격증 등)에 적용 가능해야 한다

    ----------------------------------------

    [초급(기초) 처리 규칙 - 매우 중요]
    - 초급(기초) 수준일수록 더 구체적인 학습 내용으로 작성해야 한다
    - 반드시 가장 기본적인 구성 요소부터 시작해야 한다

    예:
    - 영상 편집 → 컷 편집, 타임라인, 자막 넣기
    - 게임 개발 → 변수, 조건문, 간단한 게임 구조
    - 한문 → 기초 한자, 한자 읽기, 기본 문장 구조

    ----------------------------------------

    [topic 보정 규칙]
    - 만약 topic이 "기초", "기본", "일반"처럼 추상적이면,
    해당 과목에서 실제로 배우는 대표적인 세부 주제를 스스로 생성하여 사용하라

    ----------------------------------------

    [작성 규칙]
    - 반드시 정확히 {step_count}개의 단계 생성
    - 각 단계는 한 줄 문장으로 작성

    ❗ 매우 중요:
    - 반드시 "구체적인 개념, 기술, 작업"이 포함되어야 한다
    - 절대 추상적인 표현만 쓰지 마라

    금지 표현:
    - "기초 개념"
    - "이해하기"
    - "익히기"
    - "학습하기"
    - "단계 1", "단계 2"
    - "학습 단계"

    ❗ 이런 출력은 잘못된 결과다:
    - "영상 편집 단계 1"
    - "게임 개발 단계 2"

    ----------------------------------------

    [학습 흐름 규칙]
    - 난이도는 점진적으로 상승해야 한다
    - 각 단계는 이전 단계와 자연스럽게 이어져야 한다

    ----------------------------------------

    [좋은 예]
    - "영상 컷 편집 도구를 사용하여 기본 영상 자르기 수행"
    - "기초 한자 50자를 읽고 쓰는 방법 학습"
    - "변수와 조건문을 활용한 간단한 게임 로직 구현"

    ----------------------------------------

    [출력 규칙]
    - 반드시 JSON 배열만 출력
    - 반드시 {step_count}개의 항목 포함
    - JSON 외 텍스트 절대 금지

    ----------------------------------------

    [출력 예시]
    ["내용1", "내용2", "내용3", "내용4", "내용5", "내용6"]
    """
    # GPT 호출
    response = llm.invoke(prompt)
    #llm에게 prompt를 보내서, 결과를 받아옴
    #invoke = 호출하다/실행하다.


    try: #try~except 구문. 에러가 나도 서버가 죽지 않게 except로 막아둠
        
        curriculum_list = json.loads(response.content.strip())
        # curriculum_list = json.loads(response.content) 에서 변경
        # response.content는 GPT가 준 답변 문자열
        # json.loads()는 그 문자열을 파이썬 리스트로 바꿔준다
        
         # 강제 검증
        if len(curriculum_list) != step_count:
            raise ValueError("단계 수 불일치")

        
    except:
        curriculum_list = [f"{topic} 학습을 위한 단계 {i+1}" for i in range(step_count)]
        # fallback 시 category 대신 topic 사용
        # category는 범위가 넓어 사용자 의도를 반영하지 못함 → topic으로 정확도 보완
        
        
                
    # 결과 반환
    return curriculum_list #문자열이 아니라, 진짜 list 반환.  curriculum_service.py 에서 그대로 받아씀


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

    ❗ 매우 중요:
    - 절대 추상적인 표현을 사용하지 마라

    금지 표현:
    - "기초"
    - "공부"
    - "학습"
    - "기본 개념"
    - "이해하기"

    👉 만약 입력이 추상적이라도,
    해당 분야에서 일반적으로 배우는 구체적인 주제로 변환하라

    예:
    - "플로리스트 배우고 싶어" → "꽃다발 제작"
    - "한문 기초 배우고 싶어" → "기초 한자 읽기"
    - "랭체인 배우고 싶어" → "체인 구조", "프롬프트 연결 방식"

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
    {{"category": "파이썬", "topic": "기본 문법", "level": "초급"}}
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