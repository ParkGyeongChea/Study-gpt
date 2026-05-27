#question_node.py

#현재 step 관련 추가 질문 답변 , review 와 다르다
#review = 같은 강의 다시 설명, question = 현재 개념에 대한 추가 질문

# 현재 학습 중인 step 기반 추가 질문 처리 node

#=============================================

from services.explain_service import generate_question_answer


# 현재 학습 상태 기반 추가 질문 처리
def question_node(state):

    # 현재 학습 상태 가져오기
    category = state["category"]
    topic = state["topic"]
    level = state["level"]
    current_step = state["current_step"]

    # 사용자 질문 가져오기
    message = state["message"]

    # 현재 step 기반 질문 답변 생성
    lecture = generate_question_answer(
        category=category,
        topic=topic,
        step=current_step,
        level=level,
        question=message
    )

    # GraphState response 업데이트
    return {
        "response": lecture
    }