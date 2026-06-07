#next_step_node.py

#다음 단계 이동 담당 노드.
#현재 state 기반으로, 현재 step 읽고, 다음 step 저장

from services.graph.graph_state import GraphState


#다음 학습 단계 이동 담당 node
def next_step_node(state: GraphState):
    
    current_step = state["current_step"]
    next_step_number = current_step["step"] + 1
    curriculum = state["curriculum"]
    next_step = curriculum[next_step_number - 1]
    
    # 마지막 step 검사
    if next_step_number > len(curriculum):

        return {
            "response": "모든 학습 단계를 완료했습니다!"
        }
    
    #현재 학습 위치를 기존 step -> 다음 step 으로 변경,및 저장
    state["current_step"] = next_step
    
    
    return state