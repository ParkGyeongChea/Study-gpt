#chat_chain.py

from langchain_core.prompts import ChatPromptTemplate
from services.shared_llm import llm

chat_prompt = ChatPromptTemplate.from_template(
    """
    너는 친절한 AI 챗봇이다.

    사용자의 질문에 자연스럽고 이해하기 쉽게 , 그리고 간단하게 답변해라.

    사용자 질문:
    {message}
    """
)

chat_chain = chat_prompt | llm