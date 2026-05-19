# agent_service.py

# 역할
# message 입력 -> intent 분석 -> 기능 분기 -> 결과 반환
# 사용자 입력을 가장 먼저 판단하는 중앙 제어 서비스 파일
# 현재는 JWT 인증으로 확인된 user_id와 DB 연결(db)을 함께 받아서
# 사용자별 학습 상태를 DB 기준으로 조회/수정한다.

from services.llm_service import analyze_intent
from services.curriculum_service import (start_study_service,get_next_step,)
from services.explain_service import (explain_service,generate_step_lecture)
from services.quiz_service import generate_quiz
from services.session_service import (get_study_session,update_step_index,update_current_step)
from services.chat_message_service import save_chat_message
from services.room_service import (generate_room_title, update_room_title) #채팅방 관련 기능 파일 
from services.chat_message_service import get_chat_messages #특정 room의 기존 채팅 메시지 목록 조회
from services.chat_service import chat_service

#===================================================================

# 1. 사용자 입력을 가장 먼저 받아서, 무슨 기능을 실행할지 판단하는 중앙 제어 함수.
def run(db, user_id: int, room_id: int, message: str, study_mode: str = None):
    # 사용자 입력을 받아 intent 분석 후 기능을 분기하고,
    # 현재 로그인 사용자(user_id)와 DB 연결(db)을 함께 전달하는 AI 기능 중앙 제어 함수
    
    #현재 room의 기존 메시지 가져오기 , 이 아래 코드는 제목을 자동 생성하는 코드이기 때문이기떄문에,
    #메시지가 저장되기 전에 , 첫 메시지라고 판단을 할수 있게끔 함
    messages = get_chat_messages(db, room_id)
    
    #첫 메시지인지 확인 , 메시지 개수가 0개면,
    if len(messages) == 0:
        
        #사용자 첫 메시지 기반 제목 생성 , gpt에게 제목 생성 요청
        new_title = generate_room_title(message)
        
        #실제 DB room 제목 수정
        update_room_title(db, room_id, new_title)
    
    #현재 로그인 사용자의 메시지를 chat_message테이블에  저장
    save_chat_message(db,user_id,room_id,"user",message)
    
    
    # =========================
    # 다음 단계 요청 처리
    # =========================

    if message.strip() in ["다음", "다음 단계", "계속"]:
        # 현재는 임시로 if문 사용
        # 추후에는 LLM에게 자연어 의도 판단을 맡기는 방식 사용 가능
        # 예: LangChain / Agent 방식

        # ===== 현재 로그인 사용자의 학습 상태 가져오기 =====
        session = get_study_session(db, user_id)
        # session_service.py 파일(사용자 학습 상태를 DB에서 조회하는 역할)의
        # get_study_session 함수 호출
        # 이제 학습 상태는 study_session = {} 딕셔너리에서 가져오는 게 아니라,
        # StudySession DB 테이블에서 현재 로그인 사용자(user_id) 기준으로 조회한다.


        # ====== 학습 상태 존재 여부 예외처리 검사 ========
        if session is None:
            # DB에 현재 로그인 사용자의 학습 상태가 아직 없다는 뜻
            # 즉, 사용자가 먼저 학습을 시작하지 않고 "다음"을 입력한 경우
            return {
                "message": "먼저 학습하고 싶은 내용을 알려주세요."
            }

        # ===== 현재 저장된 학습 상태 가져오기 =====

        curriculum = session.curriculum
        # DB에 저장된 전체 커리큘럼 가져오기
        # session은 딕셔너리가 아니라 StudySession ORM 객체이므로
        # session["curriculum"]이 아니라 session.curriculum 방식으로 접근한다.

        current_step_index = session.current_step_index
        # DB에 저장된 현재 학습 단계 index 가져오기
        # index는 0부터 시작한다.
        # 예: 0 = 첫 번째 단계, 1 = 두 번째 단계

        curriculum[current_step_index]["completed"] = True
        # 리스트 + 딕셔너리 접근
        # curriculum[current_step_index] = 커리큘럼 리스트 안에서 현재 step 객체를 꺼냄
        # ["completed"] = 현재 step 객체 안의 completed 값을 수정
        # 사용자가 "다음"으로 넘어가면, 현재 단계는 학습 완료 처리한다.

        # =========== 다음 step 가져오기 ==============
        next_step = get_next_step(
            curriculum,
            current_step_index
        )
        # curriculum_service.py 파일(현재 index 기준으로 다음 step을 계산하는 역할)의
        # get_next_step 함수 호출
        # 현재 위치 기준으로 다음 step 객체를 반환한다.

        # 마지막 단계까지 완료한 경우
        if next_step is None:
            return {
                "message": "모든 학습 단계를 완료했습니다."
            }

        #======== 현재 step 위치 업데이트 ==========

        new_index = current_step_index + 1
        # 현재 index에서 1을 더해서 다음 단계 index를 만든다.

        update_step_index(db, user_id, new_index)
        # session_service.py 파일(사용자 학습 단계 index를 DB에서 수정하는 역할)의
        # update_step_index 함수 호출
        # 현재 로그인 사용자의 current_step_index 값을 DB에 저장한다.

        update_current_step(db, user_id, next_step)
        # session_service.py 파일(현재 학습 step 객체를 DB에서 수정하는 역할)의
        # update_current_step 함수 호출
        # 현재 로그인 사용자의 current_step 값을 next_step으로 DB에 저장한다.

        #========== progress(학습 진행도) 기능 ========

        total_steps = len(curriculum)
        # 전체 커리큘럼 단계 수 계산

        current_step_number = new_index + 1
        # 사용자에게 보여줄 현재 단계 번호 계산
        # index는 0부터 시작하지만, 사용자에게는 1단계부터 보여줘야 하므로 +1

        progress_percent = int((current_step_number / total_steps) * 100)
        # 진행률 퍼센트 계산
        # (현재 단계 번호 / 전체 커리큘럼 단계 수) * 100

        session.progress = progress_percent
        # 현재 로그인 사용자의 progress 값을 수정
        # 이 시점에서는 ORM 객체 값만 바뀐 상태이고,
        # 실제 DB 저장은 아래 db.commit()에서 확정된다.

        db.commit()
        # progress 수정 내용을 실제 DB에 저장

        db.refresh(session)
        # DB에 저장된 최신 상태를 다시 session 객체에 반영

        print(new_index)
        # 테스트용 단계 저장 출력 코드
        # 나중에 실제 서비스 단계에서는 제거 가능

        #========= 다음 step 강의 생성 =============
        lecture = generate_step_lecture(
            category=session.category,
            topic=session.topic,
            step=next_step,
            level=session.level
        )
        # explain_service.py 파일(현재 step 기준 강의 생성 역할)의
        # generate_step_lecture 함수 호출
        # DB에서 가져온 category/topic/level과 다음 step을 이용해서 GPT 강의를 생성한다.

        #AI 강의 응답을 chat_message 테이블에 저장
        save_chat_message(db,user_id,room_id,"assistant",lecture["content"])
    
    
        #========= light_quiz 모드 퀴즈 생성 =============
        quiz = None
        # 기본값은 None
        # free 모드에서는 퀴즈를 생성하지 않음

        if session.study_mode == "light_quiz":
            # 현재 학습 모드가 light_quiz인지 검사

            quiz = generate_quiz(db, user_id)
            # quiz_service.py 파일(현재 학습 상태 기준 퀴즈 생성 역할)의
            # generate_quiz 함수 호출
            # 현재 구조에서는 DB에서 현재 로그인 사용자의 session을 조회해야 하므로
            # db와 user_id를 함께 전달한다.
            # 단, quiz_service.py도 generate_quiz(db, user_id) 구조로 수정되어 있어야 한다.

        # 최종 반환
        return {
            "current_step": next_step,
            "lecture": lecture,
            "quiz": quiz,
            "progress": {
                "current": current_step_number,
                "total": total_steps,
                "percent": progress_percent
            }
        }

    # =========================
    # 강의 재요청 처리
    # 현재 학습 단계 반복 학습 가능 함수
    # =========================

    if "다시" in message or "모르겠어" in message:

        # ===== 현재 로그인 사용자의 학습 상태 가져오기 =====
        session = get_study_session(
            db,
            user_id
        )
        # session_service.py 파일(사용자 학습 상태를 DB에서 조회하는 역할)의
        # get_study_session 함수 호출

        # ====== 학습 상태 존재 여부 예외처리 검사 ========
        if session is None:
            # DB에 저장된 학습 상태가 없으면 다시 설명할 현재 단계도 없음
            return {
                "message": "먼저 학습하고 싶은 내용을 알려주세요."
            }

        # ====== 현재 저장된 학습 상태 가져오기 ======
        curriculum = session.curriculum
        # DB에 저장된 전체 커리큘럼 가져오기

        current_step_index = session.current_step_index
        # DB에 저장된 현재 학습 단계 index 가져오기

        current_step = curriculum[current_step_index]
        # 현재 사용자가 배우고 있는 step 데이터 가져오기

        # 현재 step 강의 다시 생성
        lecture = generate_step_lecture(
            category=session.category,
            topic=session.topic,
            step=current_step,
            level=session.level
        )
        # explain_service.py 파일(현재 step 기준 강의 생성 역할)의
        # generate_step_lecture 함수 호출
        # "다시", "모르겠어" 요청에서는 다음 단계로 이동하지 않고
        # 현재 step 기준으로 강의를 다시 생성한다.


        #AI 강의 응답을 chat_message 테이블에 저장
        save_chat_message(db,user_id,room_id,"assistant",lecture["content"])

        #========== progress(학습 진행도) 기능 ========

        total_steps = len(curriculum)
        # 전체 커리큘럼 단계 수 계산

        current_step_number = current_step_index + 1
        # 현재 단계 번호 계산
        # index는 0부터 시작하므로 사용자 표시용으로 +1

        progress_percent = int((current_step_number / total_steps) * 100)
        # 진행률 퍼센트 계산
        # "다시" 요청은 단계 이동이 아니므로 DB progress를 새로 저장하지 않고
        # 현재 위치 기준 진행률만 응답에 포함한다.

        # 반환
        return {
            "current_step": current_step,
            "lecture": lecture,
            "progress": {
                "current": current_step_number,
                "total": total_steps,
                "percent": progress_percent
            }
        }

    # =========================
    # 일반 intent 분석
    # =========================

    intent = analyze_intent(message)
    # llm_service.py 파일(사용자 입력 의도 분석 역할)의 analyze_intent 함수 호출
    # study / explain / quiz / chat 중 어떤 요청인지 판단한다.

    print("intent:", intent)

    # =========================
    # study 요청
    # =========================

    if intent == "study":

        if study_mode is None:
            # 사용자가 공부 요청은 했지만 아직 학습 모드를 선택하지 않은 경우
            # 바로 학습을 시작하지 않고, 프론트에 모드 선택 UI를 띄울 수 있는 응답을 반환한다.

            return {
                "type": "mode_select",
                "message": "어떤 학습 모드로 진행할까요?",
                "modes": [
                    {
                        "id": "free",
                        "title": "자유 학습 모드",
                        "description": "퀴즈 없이 강의 중심으로 학습합니다."
                    },
                    {
                        "id": "light_quiz",
                        "title": "가벼운 확인 모드",
                        "description": "각 챕터가 끝난 뒤 간단한 문제를 제공합니다."
                    },
                    {
                        "id": "strict_quiz",
                        "title": "집중 학습 모드",
                        "description": "문제를 통과해야 다음 단계로 진행 가능합니다."
                    }
                ]
            }

        # =========================
        # 학습 시작 처리
        # =========================

        study_result = start_study_service(
            db=db,
            # 현재 DB 연결 전달

            user_id=user_id,
            # JWT 인증으로 확인된 현재 로그인 사용자 id 전달

            room_id=room_id,
            
            message=message,
            # 사용자 입력 메시지 전달

            study_mode=study_mode
            # 사용자가 선택한 학습 모드 전달
        )
        # curriculum_service.py 파일(학습 시작 처리 역할)의
        # start_study_service 함수 호출
        # category/topic/level 분석, 커리큘럼 생성, 첫 강의 생성,
        # 그리고 StudySession DB 저장까지 이어진다.
        
        #=======================
        # AI 강의 응답 저장
        #=======================
        
        if "lecture" in study_result: #의미 = lecture 가 있을 때만 AI강의 내용을 저장, lecture가 없으면 저장하지 않고 그냥 반환
            save_chat_message( #lecture = ai가 생성한 강의 내용
                db,
                user_id,
                room_id,
                "assistant",
                study_result["lecture"]["content"]
            ) 
        
        return study_result

    # explain 요청
    elif intent == "explain":

        response = explain_service(message)

        save_chat_message(
            db,
            user_id,
            room_id,
            "assistant",
            response["content"]
        )

        return {
            "lecture": response
        }


    # quiz 요청
    elif intent == "quiz":
        return {
            "lecture": {
                "content": "퀴즈 기능 준비중"
            }
        }

    # 일반 대화
    else:
        response = chat_service(message)
        
        save_chat_message(
            db,
            user_id,
            room_id,
            "assistant",
            response["content"]
        )
        
        return {
            "lecture": {
                "content": response["content"]
            }
        }