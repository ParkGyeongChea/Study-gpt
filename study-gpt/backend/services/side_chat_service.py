# side_chat_service.py

#사이드챗 기능
#메인 채팅에서 발생하는 간단 질문들을 해소하는 채팅탭.

# ********메인 학습 흐름과는 별도로 동작하는 보조 질문용 채팅 기능*******

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.5
)

#1. 사이드챗 함수 생성

def generate_side_chat(message: str):
    prompt = f"""
        너는 초보자를 도와주는 AI 보조 튜터다.

        사용자 질문:
        {message}

        규칙:
        - 짧고 쉽게 설명하라
        - 어려운 용어 최소화
        - 필요하면 간단한 예시 포함
        - 너무 길게 설명하지 마라
    """
        
    response = llm.invoke(prompt)

    return response.content.strip()