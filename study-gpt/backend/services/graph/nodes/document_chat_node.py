#document_chat_node.py


# 여기서 이 node 가 하는 역할은:

# 1. vector_store 가져오기
# 2. similarity_search 수행
# 3. 검색 chunk 합치기
# 4. document_chat_chain 실행
# 5. state["response"] 저장


# 업로드 문서 기반
# 문서 요약 / 문서 질문 응답 Node
#=================================================

from services.rag_service import (search_similar_documents)
from services.chains.document_chat_chain import (document_chat_chain)


def document_chat_node(state):

    print("=== DOCUMENT CHAT NODE ===")

    # 현재 vector_store 가져오기
    vector_store = state.get("vector_store")

    # 사용자 메시지 가져오기
    message = state["message"]


    # 문서 검색 수행
    docs = search_similar_documents(vector_store, message)

    print("RAG DOC COUNT:",len(docs))

    # 검색된 문서 내용 연결
    context = "\n\n".join([
        doc.page_content
        for doc in docs

    ])

    print("===== RAG CONTEXT =====")
    print(context[:3000])
    print("=======================")

    
    # Chain 실행
    response = document_chat_chain.invoke({
        "context": context,
        "message": message

    })

    # GPT 응답 텍스트 정리
    content = response.content.strip()

    content = content.replace(
        "\\n",
        "\n"
    )

    # GraphState 응답 저장
    state["response"] = {
        "type": "document_chat",
        "content": content
    }

    return state