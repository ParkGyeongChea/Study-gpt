#next_step_node.py

#다음 단계 이동 담당 노드.
#현재 state 기반으로, 현재 step 읽고, 다음 step 저장

from services.graph.graph_state import GraphState


#다음 학습 단계 이동 담당 node
def next_step_node(state: GraphState):
    
    #현재 사용자가 어디 배우는 중인지 가져오기
    current_step = state["current_step"]
    
    #현재 step 번호에서 +1 해서 다음 단계 번호 계산
    next_step_number = current_step["step"] + 1
    
    #전체 커리큘럼 목록 가져오기
    curriculum = state["curriculum"]
    
    # curriculum 안의 다음 step 객체 가져오기
    next_step = curriculum[next_step_number - 1]
    
    # 마지막 step 검사
    if next_step_number > len(curriculum):

        return {
            "response": "모든 학습 단계를 완료했습니다!"
        }
    
    #현재 학습 위치를 기존 step -> 다음 step 으로 변경,및 저장
    state["current_step"] = next_step
    
    
    return state