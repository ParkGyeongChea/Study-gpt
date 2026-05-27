#review_node.py

# 현재 current_step + 현재 curriculum + 기존 학습 내용 을 기반으로 설명함

# 상태 기반 설명의 첫 번쨰 핵심 Node

# 현재 학습 중인 step 기준으로 다시 설명 생성, 현재 step 재설명 node

#===================

# 현재 학습 중인 step를 다시 설명하는 Node

from services.explain_service import generate_review_lecture


def review_node(state):

    # 현재 AI가 기억 중인 학습 상태 가져오기
    category = state["category"]
    topic = state["topic"]
    level = state["level"]
    current_step = state["current_step"]

    # 현재 step 복습 설명 생성
    lecture = generate_review_lecture(
        category=category,
        topic=topic,
        step=current_step,
        level=level
    )

    # GraphState response 업데이트
    return {
        "response": lecture
    }