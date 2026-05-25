# chat_service.py

# 역할:
# 일반 자유 대화 전용 GPT 응답 서비스
from services.chains.chat_chain import chat_chain

# 일반 대화 생성 함수
def chat_service(message: str):
    
    response = chat_chain.invoke({
        "message": message
    })

    # 최종 응답 반환
    return {

        "type": "chat",

        "content": response.content.strip()

    }