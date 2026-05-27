#chat_node.py
#일반 채팅 노드

#state 읽고 수정,반환하는 Node 구조 준비
#현재 Graph 상태 구조 사용
from services.graph.graph_state import GraphState


#chat 흐름 담당  Node
def chat_node(state: GraphState):

    #임시로 , chat 흐름 도착 성공 표시
    state["response"] = "chat mode"

    return state