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
        
                
    # 결과 반환
    return curriculum_list #문자열이 아니라, 진짜 list 반환.  curriculum_service.py 에서 그대로 받아씀
