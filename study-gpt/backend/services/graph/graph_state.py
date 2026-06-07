#graph_state.py

#랭그래프 핵심 구조 시작
# AI Agent 의 기억 공간 파일


from typing import TypedDict, Any 

# 1. 랭그래프 전체 상태 설계도, AI가 현재 기억해야 하는 데이터 목록



class GraphState(TypedDict): 
    message: str
    intent: str
    category: str
    topic: str
    level: str
    response: str
    curriculum: list 
    current_step: dict 
    learning_intent: str 
    user_id: int 
    room_id: int 
    db: object 
    learning_status: str 
    vector_store: Any
    

    
    