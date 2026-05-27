#finish_node.py

# 학습 종료 처리 Node

from services.session_service import update_learning_status

def finish_node(state):

    # 현재 학습 상태를 finished 로 변경
    state["learning_status"] = "finished"
    
    # 현재 학습 상태를 DB에도 저장
    update_learning_status(
        db=state["db"],
        user_id=state["user_id"],
        room_id=state["room_id"],
        learning_status="finished"
    )

    # 사용자 응답 저장
    state["response"] = (
        "현재 학습을 종료합니다.\n\n"
        "수고하셨습니다! :) "
    )

    return state