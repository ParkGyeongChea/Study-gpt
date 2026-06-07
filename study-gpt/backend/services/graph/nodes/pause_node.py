#pause_node.py

# 학습 일시정지 처리 Node

from services.session_service import update_learning_status


def pause_node(state):

    
    state["learning_status"] = "paused"
    
    # 현재 학습 상태를 DB에도 저장
    update_learning_status(
        db=state["db"],
        user_id=state["user_id"],
        room_id=state["room_id"],
        learning_status="paused"
    )

    # 사용자 응답 저장
    state["response"] = (
        "학습을 잠시 중단할게요.\n\n"
        "나중에 다시 이어서 학습할 수 있습니다."
    )

    return state