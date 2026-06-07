#intent_node.py

#사용자 의도 분석 node
# 이 노드는 아래의 역할을 가짐.
# 1. State 받기
# 2. 사용자 message 읽기
# 3. intent 분석
# 4. State에 intent 저장
# 5. 수정된 State 반환
#=================================

#이 Node가 사용할 상태 구조 가져오기
from services.graph.graph_state import GraphState

#의도 분석 AI 함수 가져오기
from services.llm_service import analyze_intent





# 1. 현재 AI agent 의 기억 상태 저장 함수, 현재 기억 상태를 의미

def intent_node(state: GraphState):
    
    message = state["message"]
    intent_result = analyze_intent(message)
    state["intent"] = intent_result
    
    return state

   