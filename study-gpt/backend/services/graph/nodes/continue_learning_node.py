#continue_learning_node.py

#category,topic,revel,current_step 기반으로 심화 설명 생성

# 현재 학습 중인 step를
# 더 깊고 자세하게 설명하는 Node

#=====================================

from services.explain_service import (
    generate_continue_learning_lecture
)


# 현재 step 기반 심화 설명 생성 node
def continue_learning_node(state):

    # 현재 학습 상태 가져오기
    category = state["category"]
    topic = state["topic"]
    level = state["level"]
    current_step = state["current_step"]


    ## 현재 step 심화 설명 생성
    lecture = generate_continue_learning_lecture(
        category=category,
        topic=topic,
        step=current_step,
        level=level
    )


    # GraphState response 업데이트
    return {
        "response": lecture
    }