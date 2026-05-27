#learning_flow_graph.py

# learning_intent_node learning_route next_step_node review_node quiz_node pause_node finish_node
# 하나의 graph로 연결하는 파일 . 
# 학습 진행 전용 Graph , 사용자가 후속 입력 보냈을 때만 실행되는 구조.

#==========================================

from langgraph.graph import StateGraph, END

from services.graph.graph_state import GraphState

from services.graph.nodes.learning_intent_node import learning_intent_node
from services.graph.nodes.next_step_node import next_step_node
from services.graph.nodes.review_node import review_node
from services.graph.nodes.continue_learning_node import continue_learning_node
from services.graph.nodes.question_node import question_node
from services.graph.nodes.document_chat_node import document_chat_node
from services.graph.nodes.quiz_node import quiz_node
from services.graph.nodes.pause_node import pause_node
from services.graph.nodes.finish_node import finish_node
from services.graph.nodes.explain_node import explain_node
from services.graph.nodes.unknown_intent_node import unknown_intent_node
from services.graph.routes.learning_route import route_learning_flow


# 1.GraphState 기반 LangGraph 생성
graph = StateGraph(GraphState) #learning_flow_graph 전용 상태 흐름 생성


# 2.node 등록
graph.add_node("learning_intent_node", learning_intent_node)
graph.add_node("explain_node", explain_node)
graph.add_node("next_step_node", next_step_node)
graph.add_node("review_node", review_node)
graph.add_node("continue_learning_node", continue_learning_node)
graph.add_node("question_node", question_node)
graph.add_node("document_chat_node", document_chat_node)
graph.add_node("quiz_node", quiz_node)
graph.add_node("pause_node", pause_node)
graph.add_node("finish_node", finish_node)
graph.add_node("unknown_intent_node", unknown_intent_node)


# 3.Entry point 설정
graph.set_entry_point("learning_intent_node")
#사용자 후속 입력 -> learning_intent_node 분석부터 시작


# 4.Conditional Route
graph.add_conditional_edges(
    "learning_intent_node",
    route_learning_flow
)
# learning_intent_node 실행 -> state["learning_intent"] 생성 -> route_learning_flow(state) -> 다음 node 자동 결정


# 5. Edge 연결
graph.add_edge("next_step_node", "explain_node")
graph.add_edge("review_node", END)
graph.add_edge("continue_learning_node", END)
graph.add_edge("explain_node", END)
graph.add_edge("quiz_node", END)
graph.add_edge("pause_node", END)
graph.add_edge("finish_node", END)
graph.add_edge("unknown_intent_node",END)
graph.add_edge("question_node", END)
graph.add_edge("document_chat_node", END)


# 6.copile
app = graph.compile()



#실행 명령 (백엔드 폴더 위치에서)
#python -m services.graph.learning_flow_graph