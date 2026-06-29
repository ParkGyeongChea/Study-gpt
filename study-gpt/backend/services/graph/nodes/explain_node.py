#explain_node.py

#현재 current_step 기반으로 강의 생성하는 node
#이 node 안에서는  generate_step_lecture() 호출


from services.graph.graph_state import GraphState
from services.explain_service import generate_step_lecture #실제 강의 생성 함수 가져오기


#explain_node 함수 생성 , 강의 생성 담당 Node
def explain_node(state: GraphState):
    
    print("=== EXPLAIN NODE RUNNING ===")
    
    #현재 학습 중인 step 정보 가져오기
    current_step = state["current_step"]
    
    #카테고리, 토픽, curret_step, level 기반으로 실제 GPT 강의 생성 수행.
    #기존 explain_service 흐름을 LangGraph 안으로 가져옴
    lecture = generate_step_lecture(
        category=state["category"],
        topic=state["topic"],
        step=current_step,
        level=state["level"],
        message=state["message"],
        study_mode=state.get("study_mode"),
        vector_store=state.get("vector_store")
    )
        
    #저장. 생성된 강의 내용을 response에 저장
    state["response"] = lecture
    
    return state