#learning_intent_node.py

#현재 학습 의도 분석 담당
#사용자 입력 + 현재 학습 상태를 기반으로 gpt에게 이 사용자는 지금 뭘 하려는지 파악하고, state["learning_intent"]에 저장
# 현재 학습 흐름 의도를 분석하는 Node

from services.chains.learning_intent_chain import analyze_learning_intent


def learning_intent_node(state):

    message = state["message"]
    current_step = state["current_step"]

    # GPT 기반 학습 의도 분석
    learning_intent = analyze_learning_intent(
        message=message,
        current_step=current_step
    )

    # GraphState 업데이트
    return {
        "learning_intent": learning_intent
    }