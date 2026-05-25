#study_graph.py

#LangGraph 전체 흐름 조립을 담당.
#어떤 Node를 쓸지 어떤 순서로 연결할지 어디서 시작할지 정의.

#여기서부터 StateGraph 개념 등장. 
#StateGraph = 상태(state)기반 AI 흐름 설계기

#예전 구조는 if/else 중심 흐름. 
#랭그래프 구조는 node-> state변경-> 다음 node흐름
#즉, AI agent 자제를 그래프 형태로 조립.

#===================================

from langgraph.graph import StateGraph, END
#StateGraph = 랭그래프 흐름 설계 객체(Node추가, 흐름 연결, 시작점 연결 등을 담당)
#END = 그래프 종료 지점

from services.graph.graph_state import GraphState #이 그래프에서 사용할 상태 구조 가져오기
#END = 그래프 종료 지점

from services.graph.nodes.intent_node import intent_node #의도 분석 node 가져오기



# 1.GraphState구조를 사용하는 LangGraph 흐름 생성
graph = StateGraph(GraphState)

#LangGraph에 행동(Node) 등록. 
graph.add_node("intent_node", intent_node)
#첫번쨰 intent_node = graph 내부에서 사용할 node 이름
#두번째 intent_node = 만들어둔 def intent_node(state): 를 의미.
#즉, 이 이름을 이 함수를 등록해라 라는 뜻.

# 2. Entry Point(랭그래프 시작 노드) 설정

graph.set_entry_point("intent_node") #그래프 실행 시, intent_node 부터 시작

# 3. 종료 지점(END) 설정 , 여기서 흐름을 종료한다 라는 특수 지점.
graph.add_edge("intent_node", END)
#intent_node 실행 후, graph 종료

# 4. 현재까지 만든 node, edge, 시작점, 종료점 전부 조립해서, 실행 가능한 랭그래프 객체 생성
app = graph.compile()
#여기서 app은, 실제 AI Agent 실행 객체가 됨.

#======임시 테스트 코드=======
#graphstate 실제 데이터 만들기.(현재 그래프가 사용할 상태 객체)
test_state = {
    "message": "파이썬 배우고 싶어",
    "intent": "",
    "category": "",
    "topic": "",
    "level": "",
    "response": ""
}

#현재 graph 실행
result = app.invoke(test_state)

print(result)


#실행 명령 (백엔드 폴더 위치에서)
#python -m services.graph.study_graph