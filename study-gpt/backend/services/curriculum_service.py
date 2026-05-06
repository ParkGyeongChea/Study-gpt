#curriculum_service.py

#=========================================

# study_router.py가 받은 요청을 넘겨주면,
# curriculum_service.py가 그 요청을 해석해서
# 카테고리와 커리큘럼 결과를 만들어주는 파일
# 생성된 결과를 서비스에서 사용하기 좋은 형태로 가공
# 처리 담당

# start_study_service
# → analyze_user_input으로 분석
# → generate_curriculum으로 생성

#=========================================

# curriculum_service.py


from services.llm_service import generate_curriculum
from services.llm_service import analyze_user_input
from services.explain_service import generate_step_lecture


# 1. 사용자의 학습 요청을 처리하는 함수.
# agent_service.py에서 intent가 "study"로 판단되면 이 함수가 실행된다.
def start_study_service(message: str):
    
    
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
    # GPT가 생성한 커리큘럼 문자열 리스트 반환



    # 6. 커리큘럼을 step 객체 구조로 변환
    
    curriculum = parse_curriculum(curriculum)
    # 기존 문자열 리스트 형태의 curriculum 데이터를
    # step 번호, 제목, 완료 여부 등을 가진 객체 구조로 변환
    # 같은 변수명을 다시 사용하는 이유:
    # parse 전후 모두 "커리큘럼 데이터"라는 역할은 동일하기 때문
    # 단, 내부 데이터 구조는 문자열 리스트 → 객체 리스트 형태로 변경됨
    
    print(type(curriculum))
    print(curriculum)
    
    #리스트는 llm_service.py 안의 def generate_curriculum(): 함수 내부
    
    #분석된 값을 llm_service.py 의 generate_curriculum()에 넘겨서 실제 커리큘럼을 만든다.
    # LLM이 다양한 분야의 커리큘럼을 생성
    # 코드는 흐름과 안정성만 관리

    # 6.커리큘럼 단계 꺼내기
    
    current_step_index = 0 # 현재 단계 번호(index)를 저장. 사용자가 배우고 있는 커리큘럼을 뜻함
    
    current_step = curriculum[current_step_index]
    #커리큘럼 리스트에서 , current_step_index 위치의 데이터를 꺼냄
    #first_step = curriculum[0] 에서 변경 (무조건 첫 번째 단계만 가져옴)
    #이제 고정된 단계가 아닌, 변경 가능한 현재 단계로 새로 설정
    
    #7. 첫 번쨰 단계 강의 생성
    first_lecture = generate_step_lecture(
        category=category,
        topic=topic,
        step=current_step,
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
        "current_step": current_step,
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


# 2. 생성된 데이터를 서비스용 구조로 가공하는 함수
#   단순 문자열 리스트 -> step 객체 리스트로 변환
def parse_curriculum(curriculum):
    
    steps = []
    
    for index, line in enumerate(curriculum): 
        #line 안에 있는 줄들을 하나씩 꺼내는 반복문
        #enumerate() = 반복하면서 번호까지 같이 꺼내주는 함수.
        
        clean_line = line.strip()
        
        if clean_line: #빈 줄이 아닌 경우메나 실행
            step_data = {
                "step" : index + 1, #현재 반복 순서(index)에 1을 더해서 단계 번호(step)로 저장
                "title" : clean_line,
                "completed" : False #학습 완료 전이니 False              
            }
            steps.append(step_data)
            
    return steps

# 3. 현재 위치를 다음 위치로 이동시키는 함수
# 사용자가 다음 커리큘럼으로 가자 라고 할떄, 이동시키는 기능을 가진 함수 ,현재는 임시 함수
def get_next_step(curriculum, current_step_index):
    
    next_step_index = current_step_index + 1
    #현재 위치에서 +1 해서 다음 단계 위치를 만듬
    
    if next_step_index < len(curriculum):
        #다음 위치가 커리큘럼 범위 안에 있는지 확인
        
        return curriculum[next_step_index]
        #다음 단계가 존재하면 그 step 객체를 꺼내서 반환
    
    return None
        
    
