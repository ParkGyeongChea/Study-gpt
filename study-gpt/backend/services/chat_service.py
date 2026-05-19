# chat_service.py

# 역할:
# 일반 자유 대화 전용 GPT 응답 서비스

from services.llm_service import llm
# llm_service.py 파일(GPT 모델 객체 관리 역할)의
# llm 객체 가져오기


# 일반 대화 생성 함수
def chat_service(message: str):

    # GPT에게 전달할 프롬프트
    prompt = f"""
    너는 친절한 AI 챗봇이다.

    사용자의 질문에 자연스럽고 이해하기 쉽게 답변해라.

    사용자 질문:
    {message}
    """


    # GPT 호출
    response = llm.invoke(prompt)


    # 최종 응답 반환
    return {

        "type": "chat",

        "content": response.content.strip()

    }