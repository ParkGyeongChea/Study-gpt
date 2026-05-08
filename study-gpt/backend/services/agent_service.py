# agent_service.py

#역할
#message 입력-> intent 분석 -> 기능 분기 -> 결과 반환
#사용자 입력을 가장 먼저 판단하는 곳

from services.llm_service import analyze_intent

# llm_service.py 의 사용자 의도(Intent) 분석 함수 import
# 사용자의 입력이 study / explain / quiz / chat 중 무엇인지 판별하는 함수

from services.curriculum_service import (
    
    start_study_service,# curriculum_service.py 의 학습 시작 처리 함수
                        # 사용자 입력 분석 → 커리큘럼 생성 → 첫 step 강의 생성까지 담당
                        
    get_next_step,# curriculum_service.py 의 다음 학습 단계 반환 함수
                  # 현재 step index 기준으로 다음 step 객체를 반환
    
)

from services.explain_service import (
    
    explain_service,# explain_service.py 의 일반 설명 생성 함수
                    # 사용자의 단일 질문(explain intent)에 대한 설명 생성
                    
    generate_step_lecture # explain_service.py 의 커리큘럼 단계 강의 생성 함수
                          # 현재 step 정보를 기반으로 GPT 강의 생성

)

from services.session_service import (
    
    get_study_session, # 현재 저장된 학습 상태 가져오기
    
    update_step_index # 현재 학습 단계 index 업데이트
    
)


def run(message: str): #router 에서 이 함수를 호출함. 반드시 필요
    
    # =========================
    # 다음 단계 요청 처리
    # =========================
    
    if "다음" in message: #현재는 임시로 if문 사용. 추후에는 LLM에게 맡기는 방식 사용 -> LangChain / Agent 방식
        
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
        
        #최종 반환
        return {
            "current_step": next_step,
            "lecture": lecture,
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
        
        #반환
        return {
            "current_step": current_step,
            "lecture": lecture
        }
        

    # =========================
    # 일반 intent 분석
    # =========================
    
    intent = analyze_intent(message)
    #이 함수에서 제일 먼저 해야 할 일. intent 분석
    
    print("intent:", intent)
    
    # study 요청 
    if intent == "study":
        return start_study_service(message)
        #메세지 리턴
    
    # explain 요청
    elif intent == "explain":
        return explain_service(message)
    
    # quiz 요청
    elif intent == "quiz":
        return {"message": "퀴즈 기능 준비중"}
    
    
    # 일반 대화
    else:
        return {"message": "일반 대화 기능 준비중"}