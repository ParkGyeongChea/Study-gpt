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
    
    
    # 1.기존 학습 상태 존재 여부 검사(현재 로그인 사용자의 기존 학습 상태를 StudySession 테이블에서 조회)
    session = get_study_session(db,user_id,room_id)
    
    if session is not None:
        
        chat_history = get_chat_messages(db,room_id)
        
    
        # 기존 학습 이어하기 처리, DB에 기존 학습 상태가 존재하는 경우
        return {
            "message": "이전에 진행하던 학습을 이어서 진행합니다!",
            "category": session.category,
            "topic": session.topic,
            "level": session.level,
            "curriculum": session.curriculum,
            "current_step": session.current_step,
            "progress": session.progress,
            "chat_history": chat_history 
        }
    
    # 2. 전처리
    message = message.lower().strip()
    # 사용자 입력 정의
    #lower() 소문자 변환

    # 3. 사용자 입력 분석
    category, level, topic = analyze_user_input(message)
    
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
    



    # 7. 커리큘럼을 step 객체 구조로 변환
    
    curriculum = parse_curriculum(curriculum)
    
    
    print(type(curriculum))
    print(curriculum)
    
    

    # 8.학습 상태 저장 기능 
    current_step_index = 0 
    current_step = curriculum[current_step_index]
    
    
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
        
    )
    
    # light_quiz 모드 퀴즈 생성
    print("퀴즈 생성 시작")
    
    quiz = None
    quiz_for_user = None
    quiz_answer_data = None
   
    
    if study_mode in ["light_quiz", "strict_quiz"]:
        quiz = generate_quiz(db, user_id, room_id)
        quiz_for_user = quiz["quiz_for_user"]
        quiz_answer_data = quiz["quiz_answer_data"]
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
    
    if next_step_index < len(curriculum):
        
        return curriculum[next_step_index]
        
    
    return None
        
    
