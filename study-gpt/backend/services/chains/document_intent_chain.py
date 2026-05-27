#document_intent_chain.py

#사용자 메시지가 문서 질문인지, 문서 학습 시작인지 판단하는 파일

# document_intent_chain.py

# 업로드 문서 관련 요청 의도 분석


from langchain_core.prompts import ChatPromptTemplate
from services.shared_llm import llm


document_intent_prompt = ChatPromptTemplate.from_template(
    """
    너는 업로드된 문서를 기반으로,
    사용자의 요청 의도를 분석하는 AI 시스템이다.

    사용자는 현재 PDF 또는 문서를 업로드한 상태다.

    --------------------------------------------------

    [현재 가능한 intent 종류]

    1. document_chat
    - 문서 내용을 질문/요약/정리하려는 목적
    - 문서 기반 Q&A

    예시:
    - "이 PDF 요약해줘"
    - "문서 내용 설명해줘"
    - "이 부분 정리해줘"
    - "핵심만 알려줘"
    - "출석 규정 설명해줘"

    --------------------------------------------------

    2. document_study
    - 문서를 기반으로 학습을 시작하려는 목적
    - AI 강의 형태를 원함
    - 커리큘럼 학습 흐름 생성 목적

    예시:
    - "이 PDF로 공부할래"
    - "이 문서 기반으로 학습 시작"
    - "이 파일로 강의해줘"
    - "이걸 교재처럼 공부하고 싶어"
    - "이 문서로 수업해줘"

    --------------------------------------------------

    [매우 중요한 규칙]

    - 반드시 하나의 intent만 출력하라
    - 설명 절대 금지
    - JSON 금지
    - 코드블록 금지

    --------------------------------------------------

    사용자 메시지:
    "{message}"

    --------------------------------------------------

    반드시 아래 둘 중 하나만 출력:

    document_chat
    document_study
    """
)


document_intent_chain = document_intent_prompt | llm


# document intent 분석 함수
def analyze_document_intent(message: str):

    response = document_intent_chain.invoke({
        "message": message
    })

    return response.content.strip()