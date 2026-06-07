# quiz_node.py

# 현재 학습 중인 step 기준으로 퀴즈 생성

# 현재 학습 step 기준 퀴즈 생성 Node

from services.quiz_service import generate_quiz


def quiz_node(state):

    # 현재 학습 상태 가져오기
    category = state["category"]
    topic = state["topic"]
    level = state["level"]
    current_step = state["current_step"]

    # 현재 step 기준 퀴즈 생성
    quiz = generate_quiz(
        category=category,
        topic=topic,
        step=current_step,
        level=level
    )

    # GraphState response 업데이트
    return {
        "response": {
            "quiz_for_user": quiz["quiz_for_user"], 
            "quiz_answer_data": quiz["quiz_answer_data"] 
        }
    }