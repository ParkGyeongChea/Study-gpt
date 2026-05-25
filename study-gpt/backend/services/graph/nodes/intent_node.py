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


#Node는 직접 GPT 호출을 하지 않는다


# 1. 현재 AI agent 의 기억 상태 저장 함수, 현재 기억 상태를 의미
# 여기 안에는 state["message"], state["intent"] 같은 값이 들어있음

def intent_node(state: GraphState):
    
    #현재 State 안에 저장된 사용자 입력
    message = state["message"]
    
    #이전에 만든 intent_chain.invoke() 기반 구조 실행 (prompt 생성, gpt 호출, json 파싱)
    intent_result = analyze_intent(message)
    
    #현재 AI가 분석한 state를  현재 상태 intent에 저장.
    state["intent"] = intent_result
    
    return state

    #왜 state를 반환?
    #Node 실행 -> 수정된 state 반환 -> 다음 Node 전달 구조이기 때문에.
    #즉, node는 state를 수정하고 다시 반환해야 한다.