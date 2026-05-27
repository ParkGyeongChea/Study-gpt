#curriculum_service.py

#=========================================
# 학습 흐름 제어, step 관리 ,session 저장
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
from services.session_service import save_study_session, get_study_session
from services.quiz_service import generate_quiz
from services.chat_message_service import get_chat_messages


#====================================================


# 1. 사용자의 학습 요청을 처리하는 함수.
# agent_service.py에서 intent가 "study"로 판단되면 이 함수가 실행된다.
def start_study_service(
    db,
    user_id: int,
    room_id: int,
    message: str,
    study_mode: str = "free"
):
    #=============================================================
    
    # 1.기존 학습 상태 존재 여부 검사(현재 로그인 사용자의 기존 학습 상태를 StudySession 테이블에서 조회)
    session = get_study_session(db,user_id,room_id)
    
    if session is not None:
        
        # 이전 채팅 기록 조회
        chat_history = get_chat_messages(db,room_id)
        #chat_message_service.py(이전 채팅 조회 역할 파일)의 get_chat_messages 함수 호출
        #현재 로그인 사용자의 room 기준 메시지 조회
        
        
        # 기존 학습 이어하기 처리, DB에 기존 학습 상태가 존재하는 경우
        return {
            "message": "이전에 진행하던 학습을 이어서 진행합니다!",
            "category": session.category,
            "topic": session.topic,
            "level": session.level,
            "curriculum": session.curriculum,
            "current_step": session.current_step,
            "progress": session.progress,
            "chat_history": chat_history #orm 객체 리스트 일 가능성이 있음. 프론트 연결 시 json 직렬화 처리 가능성
        }
    
    # 2. 전처리
    message = message.lower().strip()
    # 사용자 입력 정의
    #lower() 소문자 변환

    # 3. 사용자 입력 분석
    category, level, topic = analyze_user_input(message)
    # 문장을 분석해서, llm_service 의 analyze_user_input 함수를 이용해 문장을 나눈다.
    # category = "파이썬" level = "초급" topic = "파이썬 기초 전체"
        

    # 4. 단계 수 결정
    if level == "초급":
        step_count = 5
    elif level == "중급":
        step_count = 6
    else:
        step_count = 7


    # 5. 디버깅용 출력
    print("DEBUG message:", message)
    print("DEBUG category:", category)
    print("DEBUG topic:", topic)
    print("DEBUG level:", level)
    print("DEBUG step_count:", step_count)

    # 6. LLM 기반 커리큘럼 생성
    
    curriculum = generate_curriculum(category, topic, level, step_count)
    # GPT가 생성한 커리큘럼 문자열 리스트 반환



    # 7. 커리큘럼을 step 객체 구조로 변환
    
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


    # 8.학습 상태 저장 기능 
    current_step_index = 0 # 현재 단계 번호(index)를 저장. 사용자가 배우고 있는 커리큘럼을 뜻함 
    
    
    # 현재 사용자가 학습 중인 step 데이터
    current_step = curriculum[current_step_index]
    #커리큘럼 리스트에서 , current_step_index 위치의 데이터를 꺼냄
    #first_step = curriculum[0] 에서 변경 (무조건 첫 번째 단계만 가져옴)
    #이제 고정된 단계가 아닌, 변경 가능한 현재 단계로 새로 설정
    
    
    # 9. 현재 학습 상태 저장
    # 현재 사용자의 학습 진행 정보를 저장
    # 이후 진행률 관리, 다음 단계 이동 등에 활용 가능
    session = save_study_session(
        db=db,
        user_id=user_id,
        room_id=room_id,
        category=category,
        topic=topic,
        level=level,
        curriculum=curriculum,
        current_step_index=current_step_index,
        current_step=current_step,
        study_mode=study_mode,
        learning_status="learning"
    )
    
    
    # 10.첫 번쨰 단계 강의 생성 
    first_lecture = generate_step_lecture(
        category=category,
        topic=topic,
        step=current_step,
        level=level,
        message=message
        # 현재 과목, 전체 주제, 첫 번째 커리큘럼 단계, 난이도를 넘겨서 첫 번째 단계 강의 생성.
        # 현재 step를 기반으로, 실제 강의를 생성하는 기능
    )
    
    #========= light_quiz 모드 퀴즈 생성 =============
    
    print("퀴즈 생성 시작")
    
    quiz = None
    quiz_for_user = None
    quiz_answer_data = None
    # 기본값은 None
    # free 모드에서는 퀴즈를 생성하지 않음
    
    if study_mode in ["light_quiz", "strict_quiz"]:
        # 현재 학습 모드가 light_quiz인지,strict인지 검사

        quiz = generate_quiz(db, user_id, room_id)
        # 현재 step 기준으로 퀴즈 생성
        
        #quiz_for_user =사용자 화면 출력용 문제
        #quiz_answer_data = 정답 + 해설 포함 내부 데이터
        quiz_for_user = quiz["quiz_for_user"]

        quiz_answer_data = quiz["quiz_answer_data"]
        
        #현재 퀴즈 정답 상태를 DB session 에 저장, 이제 서버는 현재 문제 정답이 뭔지 기억 가능
        session.quiz_answer_data = quiz_answer_data

        db.commit()
              
      
    # 11. 최종 응답
    #최종 응답을 딕셔너리 형태로 반환한다.
    return {
        "category": category,
        "topic": topic,
        "level": level,
        "curriculum": curriculum,
        "current_step": current_step,
        "lecture": first_lecture,
        "quiz":quiz_for_user
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
# 문자열 curriculum -> step 객체 리스트 변환
def parse_curriculum(curriculum):

    steps = []

    # 문자열이면 줄 단위 분리
    if isinstance(curriculum, str):

        curriculum = curriculum.split("\n")

    for index, line in enumerate(curriculum):

        clean_line = line.strip()

        # 빈 줄 제거
        if not clean_line:
            continue

        # "1. 제목" 형태 처리
        if ". " in clean_line:

            clean_line = clean_line.split(". ", 1)[1]

        step_data = {
            "step": index + 1,
            "title": clean_line,
            "completed": False
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
        
    
