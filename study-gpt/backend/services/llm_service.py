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
    temperature=0.7
    )


def generate_curriculum(category: str, level:str, step_count:int): #이 함수는 과목 이름 하나를 받음.
    
    #GPT 지시문 , {category} 넣어 과목 바꿀수 있게 하고 JSON형식 강제
    prompt = f"""
    너는 학습자의 수준에 맞는 커리큘럼을 설계하는 전문가다.

    과목: {category}
    수준: {level}

    매우 중요한 규칙:
    - 반드시 정확히 {step_count}개의 항목을 생성해야 한다.
    - {step_count}개보다 많거나 적으면 안 된다.

    요구사항:
    1. 각 단계는 난이도가 점진적으로 상승해야 한다
    2. {level} 수준에 맞는 내용만 포함
    3. 초급 내용 절대 포함 금지 (알파벳, 기초 단어 등 금지)
    4. 각 단계는 한 줄 문장으로 작성
    5. 중복 표현 금지

    출력 규칙:
    - 반드시 JSON 배열만 출력
    - 반드시 {step_count}개의 항목 포함
    - 반드시 [ 로 시작하고 ] 로 끝날 것
    - JSON 외 텍스트 절대 금지

    잘못된 예:
    ❌ 5개만 출력
    ❌ 설명 포함
    ❌ JSON 형식 아님

    정답 예:
    ["내용1", "내용2", "내용3", "내용4", "내용5", "내용6", "내용7"]
    """
    # GPT 호출
    response = llm.invoke(prompt)
    #llm에게 prompt를 보내서, 결과를 받아옴
    #invoke = 호출하다/실행하다.


    try: #try~except 구문. 에러가 나도 서버가 죽지 않게 except로 막아둠
        
        curriculum_list = json.loads(response.content)
        # response.content는 GPT가 준 답변 문자열
        # json.loads()는 그 문자열을 파이썬 리스트로 바꿔준다
        
         # ⭐ 강제 검증
        if len(curriculum_list) != step_count:
            raise ValueError("단계 수 불일치")

        
    except:
        curriculum_list = [f"{category} 학습 단계 {i+1}" for i in range(step_count)]
        #step_count 만큼 반복하면서 카테고리 학습 단계 1,2,3 형태의 리스트를 ㅁ나듬
        
                
    # 결과 반환
    return curriculum_list #문자열이 아니라, 진짜 list 반환.  curriculum_service.py 에서 그대로 받아씀


def analyze_user_input(message: str): #사용자 입력-> 과목-> 레벨 추출 함수 추가
    prompt = f"""
    너는 사용자의 학습 요청을 분석하는 AI다.

    [사용자 입력]
    "{message}"

    [작업]
    사용자의 입력을 분석하여 다음 두 가지를 추출하라:
    1. category (과목)
    2. level (학습 수준)

    [level 규칙]
    - 초급: 입문, 처음, 기초, 초보
    - 중급: 중급, 어느 정도 경험 있음
    - 고급: 심화, 전문가 수준

    [category 선택 규칙]
    아래 목록 중 반드시 하나만 선택:
    ["코딩", "영어", "수학", "백엔드", "프론트엔드"]

    - "파이썬", "프로그래밍", "개발" → "코딩"
    - "서버", "API" → "백엔드"
    - "리액트", "UI" → "프론트엔드"

    [출력 규칙 - 매우 중요]
    - 반드시 JSON만 출력
    - JSON 외의 어떤 텍스트도 절대 출력 금지
    - 설명, 주석, 문장 절대 금지
    - 코드블록(```) 절대 사용 금지
    - 반드시 한 줄 JSON으로 출력

    [출력 형식]
    {{"category": "코딩", "level": "초급"}}
    """
    response = llm.invoke(prompt)
    
    
    try:
        result = json.loads(response.content)
        
    except:
        return "코딩", "초급"
    
    return result["category"], result["level"]

if __name__ == "__main__":
    print(analyze_user_input("파이썬 중급 배우고 싶어"))
    print(analyze_user_input("파이썬 처음 배우고 싶어"))
    print(analyze_user_input("백엔드 API 제대로 배우고 싶어"))
    print(analyze_user_input("영어 회화 중급 수준으로 공부하고 싶어"))