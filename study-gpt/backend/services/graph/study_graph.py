#study_graph.py

#LangGraph 전체 흐름 조립을 담당.
#어떤 Node를 쓸지 어떤 순서로 연결할지 어디서 시작할지 정의.

#여기서부터 StateGraph 개념 등장. 
#StateGraph = 상태(state)기반 AI 흐름 설계기

#예전 구조는 if/else 중심 흐름. 
#랭그래프 구조는 node-> state변경-> 다음 node흐름
#즉, AI agent 자제를 그래프 형태로 조립.

# 랭그래프 흐름

# 1. graph 생성
# 2. node 등록
# 3. 시작 node 설정
# 4. route 함수 작성
# 5. 조건 분기 연결
# 6. 종료 edge 연결
# 7. compile
# 8. invoke 테스트

#===================================

from langgraph.graph import StateGraph, END
#StateGraph = 랭그래프 흐름 설계 객체(Node추가, 흐름 연결, 시작점 연결 등을 담당)
#END = 그래프 종료 지점

from services.graph.graph_state import GraphState #이 그래프에서 사용할 상태 구조 가져오기
from services.graph.nodes.intent_node import intent_node #의도 분석 node 가져오기
from services.graph.nodes.study_node import study_node
from services.graph.nodes.chat_node import chat_node
from services.graph.nodes.explain_node import explain_node
from services.graph.nodes.next_step_node import next_step_node
from services.graph.nodes.learning_intent_node import learning_intent_node
from services.graph.nodes.review_node import review_node
from services.graph.nodes.quiz_node import quiz_node
from services.graph.nodes.finish_node import finish_node
from services.graph.nodes.pause_node import pause_node

from services.graph.routes.learning_route import route_learning_flow

# GraphState구조를 사용하는 LangGraph 흐름 생성
graph = StateGraph(GraphState)


# 1. LangGraph에 행동(Node) 등록. 
graph.add_node("intent_node", intent_node) 
graph.add_node("study_node", study_node)
graph.add_node("chat_node", chat_node)
graph.add_node("explain_node", explain_node)
graph.add_node("next_step_node", next_step_node)
graph.add_node("learning_intent_node", learning_intent_node)
graph.add_node("review_node", review_node)
graph.add_node("quiz_node", quiz_node)
graph.add_node("finish_node", finish_node)
graph.add_node("pause_node", pause_node)



#  Entry Point(랭그래프 시작 노드) 설정
graph.set_entry_point("intent_node") #그래프 실행 시, intent_node 부터 시작


# 현재 state를 보고 다음 node를 결정하는 함수
def route_by_intent(state: GraphState):

    #사용자 의도(intent) 꺼내오기
    intent = state["intent"]

    #intent 가 study면 study_node로 이동
    if intent == "study":
        return "study_node"

    return "chat_node"


#======시작 흐름========

#intent_node 실행 후, router_by_intent 호출 , 다음 node 자동 선택
graph.add_conditional_edges("intent_node",route_by_intent)

#=======학습 메인 흐름=======

#study_node 완료 후, explain_node 이동 
#즉 커리큘럼 생성 -> current_step 생성 후 바로 강의 생성
graph.add_edge("study_node", "explain_node")

#강의 생성 끝 -> 사용자 현재 학습 의도 분석
# graph.add_edge("explain_node", "learning_intent_node")
graph.add_edge("explain_node", END)

#learning_intent_node 실행 후, route_learning_flow(state) 결과에 따라 다음 Node 자동 이동
graph.add_conditional_edges("learning_intent_node",route_learning_flow)

#============ 분기 이후 흐름========

#next_step_node 실행 후 새 explain_node실행 , 현재는 임시 테스트 edge
graph.add_edge("next_step_node", "explain_node")

#복습 요청하면 강의 다시 생성
graph.add_edge("review_node", "explain_node")


#=======종료 edge 연결=========
graph.add_edge("quiz_node", END)
graph.add_edge("chat_node", END)
graph.add_edge("finish_node", END)
graph.add_edge("pause_node", END)





# 4. 현재까지 만든 node, edge, 시작점, 종료점 전부 조립해서, 실행 가능한 랭그래프 객체 생성
app = graph.compile()
#여기서 app은, 실제 AI Agent 실행 객체가 됨.


#실행 명령 (백엔드 폴더 위치에서)
#python -m services.graph.study_graph
