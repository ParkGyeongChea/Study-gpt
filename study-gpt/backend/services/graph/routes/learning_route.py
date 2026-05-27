#learning_route.py

#==============================


def route_learning_flow(state):
    
    # AI 판단 결과에 따라 다음 실행 Node를 결정한다
    # GPT 의도 분석 (이 사용자의 현재 학습 목표는?) ->state 저장 -> route_learning_flow 실행->if 문 비교 후 
    #아래 노드 실행
    
    learning_intent = state["learning_intent"]

    #학습 의도가 다음 단계면, 다음 단계 이동 노드 반환
    if learning_intent == "next_step":
        return "next_step_node"
    
    #학습 의도가 다시 복습
    elif learning_intent == "review":
        return "review_node"

    #학습 의도가 질문이면
    elif learning_intent == "quiz_request":
        return "quiz_node"

    #학습 의도가 학습 종료면
    elif learning_intent == "finish_learning":
        return "finish_node"

    #학습 의도가 학습 일시 정지면
    elif learning_intent == "pause_learning":
        return "pause_node"
    
    # 현재 step 더 깊게 설명
    elif learning_intent == "continue_learning":
        return "continue_learning_node"
    
    # 현재 학습 내용 관련 추가 질문
    elif learning_intent == "question":
        return "question_node"
    
    # 업로드 문서 기반 질문 / 요약
    elif learning_intent == "document_chat":
        return "document_chat_node"
    
    
    return "unknown_intent_node"
    