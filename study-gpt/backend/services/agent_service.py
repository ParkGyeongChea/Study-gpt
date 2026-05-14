# agent_service.py

#역할
#message 입력-> intent 분석 -> 기능 분기 -> 결과 반환
#사용자 입력을 가장 먼저 판단하는 곳

from services.llm_service import analyze_intent
from services.curriculum_service import (
    start_study_service,                      
    get_next_step,   
)

from services.explain_service import (
    explain_service,
    generate_step_lecture
                          
)
from services.quiz_service import generate_quiz
from services.session_service import (
    get_study_session,  
    update_step_index, 
    update_current_step 
)
#===================================================================

# 1. 사용자 입력을 가장 먼저 받아서, 무슨 기능을 실행할지 판단하는 중앙 제어 함수.
def run(db, user_id: int, message: str, study_mode: str = None): 
    # 사용자 입력을 받아 intent 분석 후 기능을 분기하고,
    # 현재 로그인 사용자(user_id)와DB 연결(db)을 함께 전달하는 AI 기능 중앙 제어 함수
    
    
    
    # =========================
    # 다음 단계 요청 처리
    # =========================
    
    if message.strip() in ["다음", "다음 단계", "계속"]: #임시 제어 코드
        #현재는 임시로 if문 사용. 추후에는 LLM에게 맡기는 방식 사용 -> LangChain / Agent 방식
        
        # ===== 현재 저장된 학습 상태 가져오기 =====
        session = get_study_session()
        
        # ====== 학습 상태 존재 여부 예외처리 검사 ========
        if "curriculum" not in session:
            
            return{
                "message" : "먼저 학습하고 싶은 내용을 알려주세요."
            }

        # ===== 현재 저장된 학습 상태 가져오기 =====
        
        curriculum = session["curriculum"]
        #현재 저장된 전체 커리큘럼 가져오기
        
        current_step_index = session["current_step_index"]
        #현재 사용자가 몇 번째 단계 배우는 중인지 가져오기
        
        
        curriculum[current_step_index]["completed"] = True
        #리스트+딕셔너리 접근 /
        # 리스트 인덱싱 (list[0] = 리스트 안에서 특정 위치 index의 데이터를 꺼냄)
        # + 딕셔너리 키값 (딕셔너리["key"]) 꺼냄
        #현재 step 객체의 completed 값을 True 로 변경. 
        # 사용자가 다음 강의로 넘어가자고 했을때 이전 강의 학습 완료 처리
        

        
        # ===========다음 step 가져오기==============
        next_step = get_next_step(
            curriculum,
            current_step_index
        #역할: 현재 위치 기준으로, 다음 step 찾기, 다음 step 객체 반환
        )

        # 마지막 단계까지 완료한 경우
        if next_step is None:
            return {
                "message": "모든 학습 단계를 완료했습니다."
            }

        #========현재 step 위치 업데이트==========
        
        new_index = current_step_index + 1
        
        update_step_index(new_index)
        # 현재 학습 위치를 한 단계 앞으로 이동시키는 기능
        # 1단계->2단계->3단계
        #이 코드가 있어야, 다음 단계 이동, 이어하기, progress, 현재 위치 기억 전부 가능함
        
        update_current_step(next_step)
        
        
        #==========progress(학습 진행도) 기능========
        
        total_steps = len(curriculum) 
        #전체 커리큘럼 단계 수 계산
        
        current_step_number = new_index + 1
        #현재 단계 번호 계산, index는 0 부터 시작하므로 +1
        
        progress_percent = int((current_step_number / total_steps) * 100)
        #진행률 퍼센트 계산
        #(현재 단계 번호 / 전체 커리큘럼 단계 수) * 100
        

        print(new_index) #테스트용 단계 저장 출력 코드 , 추후 제거

        #========= 다음 step 강의 생성=============
        lecture = generate_step_lecture(
            category=session["category"],
            topic=session["topic"],
            step=next_step,
            level=session["level"]
            # 현재 next_step 기준으로, gpt 강의 생성
        )
        
        
        #========= light_quiz 모드 퀴즈 생성 =============
        quiz = None
        # 기본값은 None
        # free 모드에서는 퀴즈가 없으므로 기본적으로 비워둠
        
        if session["study_mode"] == "light_quiz":
            # 현재 학습 모드가 light_quiz인지 검사
            
            quiz = generate_quiz()
            # 현재 step 기준으로 퀴즈 생성
            # generate_quiz() 함수는 session 안의 current_step 정보를 사용함
        
        #최종 반환
        return {
            "current_step": next_step,
            "lecture": lecture,
            "quiz":quiz,
            "progress": {
                "current": current_step_number, #현재 단계 번호
                "total": total_steps, #전체 단계 수
                "percent": progress_percent #퍼센트
            }
         
        }
        
    # =========================
    # 강의 재요청 처리, 현재 학습 단계 반복 학습 가능 함수 
    # =========================
    
    if "다시" in message or "모르겠어" in message:
        
        # ===== 현재 저장된 학습 상태 가져오기 =====
        session = get_study_session()
        
        # ====== 학습 상태 존재 여부 예외처리 검사 ========
        if "curriculum" not in session:
            
            return{
                "message" : "먼저 학습하고 싶은 내용을 알려주세요."
            }
        
        # ======현재 저장된 학습 상태 가져오기=====
        
        curriculum = session["curriculum"]
        #현재 저장된 전체 커리큘럼 가져오기
        
        
        current_step_index = session["current_step_index"]
        #현재 사용자가 몇 번째 단계 배우는 중인지 가져오기
        
        
        current_step = curriculum[current_step_index]
        #현재 사용자가 배우고 있는 step 데이터 가져오기
        
        
        #현재 step 강의 다시 생성
        lecture = generate_step_lecture(
            category=session["category"],
            topic=session["topic"],
            step=current_step,
            level=session["level"]
        )
        
        #==========progress(학습 진행도) 기능========

        total_steps = len(curriculum)
        # 전체 커리큘럼 단계 수 계산

        current_step_number = current_step_index + 1
        # 현재 단계 번호 계산
        # index는 0부터 시작하므로 +1

        progress_percent = int((current_step_number / total_steps) * 100)
        # 진행률 퍼센트 계산
                
        #반환
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
    #이 함수에서 제일 먼저 해야 할 일. intent 분석
    
    print("intent:", intent)
    
    # =========================
    # study 요청
    # =========================

    if intent == "study":

        if study_mode is None:

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
        # study_mode 저장
        # =========================

        
        

        return start_study_service( #현재 로그인 사용자 정보(user_id) 반환
            db=db,#db연결
            user_id=user_id, #유저 id
            message=message, #사용자 입력 메시지
            study_mode=study_mode #학습 모드
            
            #전부 curriculum_service.py 로 전달됨.
        )
                
    # explain 요청
    elif intent == "explain":
        return explain_service(message)
    
    # quiz 요청
    elif intent == "quiz":
        return {"message": "퀴즈 기능 준비중"}
    
    
    # 일반 대화
    else:
        return {"message": "일반 대화 기능 준비중"}