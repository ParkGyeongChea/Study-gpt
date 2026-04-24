#curriculum_service.py

# study_router.py가 받은 요청을 넘겨주면,
# curriculum_service.py가 그 요청을 해석해서
# 카테고리와 커리큘럼 결과를 만들어주는 파일
# 처리 담당

# curriculum_service.py

# from backend.services.llm_service import generate_curriculum
# from backend.services.llm_service import analyze_user_input

from services.llm_service import generate_curriculum
from services.llm_service import analyze_user_input

def start_study_service(message: str): #사용자가 입력한 message
    
    #입력 → 전처리 → 분석 → 처리 → 출력
    
    #1. 무조건 전처리 먼저.
    message = message.lower().strip() 
    #사용자가 입력한 문장을 전부 소문자로 변환, 앞뒤 공백 제거.
    #이 코드를 아래 반복문에 넣으면, 불필요하게 계속 실행되니, 함수 시작과 동시에 실행하도록 함.
    #이 코드는 데이터 전처리 과정 전처리는 가장 먼저 해야 안전.
    #정리 코드
    
    #2. 그 다음 분석
    category, level, topic = analyze_user_input(message)
    #analyze_user_input 함수 호출 .
    #message를 가지고 분석 함수 실행.
    
    
    # 2. 단계 수(step_count) 결정
    if level == "초급":
        step_count = 5
    elif level == "중급":
        step_count = 6
    else:
        step_count = 7

    # 디버깅용 출력
    print("DEBUG message:", message)
    print("DEBUG level:", level)
    print("DEBUG step_count:", step_count)

    curriculum = generate_curriculum(category, topic, level, step_count)
    #llm_service의 해당 과목의 커리큘럼을 가져와서 저장
    #함수 호출부와 정의부는 개수가 맞아야 함.
    
    # # 4. 못 찾은 경우 (에러 처리) 
    # if category is None: #끝까지 돌았는데도 과목을 못찾음(None). 아래 에러 메시지 출력
    #     return {
    #         "error": "어떤 과목인지 이해하지 못했어요.",
    #         "message": "다시 한번 입력해주세요"
    #     }

    # 5. 정상 처리 
    #과목을 찾음. if문 밖, for문에 대한 return
    return {
        "category": category,
        "topic": topic,
        "curriculum": curriculum
    }
    
if __name__ == "__main__":
    result = start_study_service("파이썬 중급 배우고 싶어")
    print(result)

    
    #“에러 return은 먼저, 정상 return은 마지막에”
    
    
    

#python -m backend.services.curriculum_service
#실행환경경로 Desktop\AI Agent\workAI\final project\study-gpt>
#프로젝트 전체 구조 실행 코드. 