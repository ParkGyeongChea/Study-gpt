#study_node.py

#study intent 도착 확인, study 흐름 담당  node

#===============
from services.graph.graph_state import GraphState
from services.llm_service import analyze_user_input 
from services.curriculum_service import generate_curriculum 

#LangGraph Node 함수 만들기
def study_node(state: GraphState):
    
    message = state["message"]
    analyze_result = analyze_user_input(message)
    state["category"] = analyze_result[0]
    state["level"] = analyze_result[1]
    state["topic"] = analyze_result[2]
    
    #현재 분석된 학습 정보 기반으로, 5단계 커리큘럼 생성
    curriculum = generate_curriculum(
    state["category"],
    state["topic"],
    state["level"],
    5 #임시 고정 커리큘럼 갯수
)   
    # 문자열 curriculum → step 객체 구조 변환
    parsed_curriculum = []

    for index, title in enumerate(curriculum):

        parsed_curriculum.append({
            "step": index + 1,
            "title": title,
            "completed": False
        })

    # GraphState 저장
    state["curriculum"] = parsed_curriculum
    
    # 첫 step 설정
    state["current_step"] = parsed_curriculum[0]
        
    return state

# study 흐름 도착 확인 후
# response 저장하고
# state 반환