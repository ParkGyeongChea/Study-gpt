#unknown_intent_node.py

#사용자가 오타, 잘못된 입력일시 오류 메시지 출력 파일


def unknown_intent_node(state):

    return {
        "response": (
            "다시 한번 말씀해 주시겠어요?\n\n"
            "정확한 학습 명령이 필요합니다!"
        )
    }