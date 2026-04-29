#curriculum_service.py

#=========================================

# study_router.py가 받은 요청을 넘겨주면,
# curriculum_service.py가 그 요청을 해석해서
# 카테고리와 커리큘럼 결과를 만들어주는 파일
# 처리 담당

# start_study_service
# → analyze_user_input으로 분석
# → generate_curriculum으로 생성

#=========================================

# curriculum_service.py


from services.llm_service import generate_curriculum
from services.llm_service import analyze_user_input
from services.explain_service import generate_step_lecture

def start_study_service(message: str):
    
    # 사용자의 학습 요청을 처리하는 함수다.
    # agent_service.py에서 intent가 "study"로 판단되면 이 함수가 실행된다.
    
    # 1. 전처리
    message = message.lower().strip()
    # 사용자 입력 정의
    #lower() 소문자 변환

    # 2. 사용자 입력 분석
    category, level, topic = analyze_user_input(message)
    # 문장을 분석해서, llm_service 의 analyze_user_input 함수를 이용해 문장을 나눈다.
    # category = "파이썬" level = "초급" topic = "파이썬 기초 전체"
        

    # 3. 단계 수 결정
    if level == "초급":
        step_count = 5
    elif level == "중급":
        step_count = 6
    else:
        step_count = 7


    # 4. 디버깅용 출력
    print("DEBUG message:", message)
    print("DEBUG category:", category)
    print("DEBUG topic:", topic)
    print("DEBUG level:", level)
    print("DEBUG step_count:", step_count)

    # 5. LLM 기반 커리큘럼 생성
    curriculum = generate_curriculum(category, topic, level, step_count)
    
    #분석된 값을 llm_service.py 의 generate_curriculum()에 넘겨서 실제 커리큘럼을 만든다.
    # LLM이 다양한 분야의 커리큘럼을 생성
    # 코드는 흐름과 안정성만 관리

    # 6. 첫 번쨰 커리큘럼 단계 꺼내기
    first_step = curriculum[0]
    
    #7. 첫 번쨰 단계 강의 생성
    first_lecture = generate_step_lecture(
        category=category,
        topic=topic,
        step=first_step,
        level=level
        #현재 과목, 전체 주제, 첫 번째 커리큘럼 단계, 난이도를 넘겨서 첫 번째 단계 강의 생성.
    )
    
    #8. 최종 응답
    #최종 응답을 딕셔너리 형태로 반환한다.
    return {
        "category": category,
        "topic": topic,
        "level": level,
        "curriculum": curriculum,
        "current_step": first_step,
        "lecture": first_lecture
    }

    #사용자는 API 응답으로 아래처럼 받는다.
    
    # {
    # "category": "파이썬",
    # "topic": "파이썬 기초 전체",
    # "level": "초급",
    # "curriculum": [
    #     "파이썬이 무엇인지 알아보기",
    #     "변수와 데이터 타입 이해하기"
    # ]
    # }
    
    
    

#python -m backend.services.curriculum_service
#실행환경경로 Desktop\AI Agent\workAI\final project\study-gpt>
#프로젝트 전체 구조 실행 코드. 