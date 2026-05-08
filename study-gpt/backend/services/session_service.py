#session_service.py

# 현재 학습 진행 상태 저장
# 이후 다음 단계 이동이나 진행률 관리 등에 사용 가능

# 현재 topic,urriculum,step,index 를 저장

#============================================================

#현재 학습 상태 저장용 변수 생성
study_session = {}


#=============학습 상태 저장 함수 ================
def save_study_session(
    category,
    topic,
    level,
    curriculum,
    current_step_index,
    current_step
):
    
    global study_session
    #글로벌 함수. 함수 안에서도 바깥 변수 수정할수 있도록 함

    study_session = {
        "cotegory": category,
        "topic": topic,
        "level": level,
        "curriculum": curriculum,
        "current_step_index": current_step_index,
        "current_step": current_step
    }
    
#======== 현재 학습 상태 반환 함수==============
def get_study_session():
    
    return study_session

# 현재 학습 단계 index 수정 함수
def update_step_index(new_index):

    global study_session

    study_session["current_step_index"] = new_index