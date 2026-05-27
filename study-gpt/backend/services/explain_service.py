#explain_service.py

from services.shared_llm import llm #설명 기능을 직접적으로 실행할 llm import

from services.rag_service import (
    search_similar_documents
)

#랭체인 실행 객체 추가
from services.chains.explain_chain import (
    explain_chain,
    explain_chat_chain,
    question_answer_chain,
    review_lecture_chain,
    continue_learning_chain
)

#1. 일반 질문용 함수 생성
def explain_service(message: str):
 
    #====
    # 기존 llm_service에서의 함수 호출은 json 파싱 실패만 막는 구문으로 try~except 사용.
    # llm.invoke(prompt) 자체도 실패할 가능성이 있어서, try~except 구문 안에 호출.
    # 문제가 생기면 response 자체가 만들어지지 않는다.
    # 그래서 explain_service 에서는 gpt 호출부터 결과 정리까지 전부 안전하게 감쌈
    
    try:
        #랭체인 프롬프트 호출
        response = explain_chat_chain.invoke({
            "message": message
        })
        
        content = response.content.strip()
        content = content.replace("\\n", "\n")

        return { #성공했을 때 결과를 딕셔너리 형태로 반환함.
            "type": "explain", #이 응답이 설명 응답이라는 표시 , 사용자가 궁금한 것을 물어봄 -> 답변
            "content": content # gpt가 실제로 만든 설명 내용
        }

    except Exception as e: 
        #try 안에서 에러가 발생하면 여기로 넘어온다.
        # Exception as e 는 발생한 에러 정보를  e라는 변수에 담는다는 뜻.
        
        return { #에러가 났을 때 기본 응답을 반환하는 코드
            "type": "explain",
            "content": "설명을 생성하는 중 문제가 발생했습니다. 다시 시도해주세요."
        }
        
        
#2. 커리큘럼 단계 강의용 함수 생성
def generate_step_lecture(category: str, topic: str, step: str, level: str, message, vector_store=None):
    #vector_store=None 넣는 이유 = RAG 검색하려면, FAISS vector db 가 필요함.
    print("=== GENERATE STEP LECTURE RUNNING ===")
    
    try:
        
        # 기본 context
        context = "참고 자료 없음"

        # RAG 문서 검색
        if vector_store:
            
            print("VECTOR STORE EXISTS")
            print("MESSAGE:", message)
            print("TOPIC:", topic)
            
            #현재 step 제목 기준으로 관련 chunk 검색 수행
            # 검색된 청크들을 하나의 문자열로 합치고, GPT에게 실제로 넣을 참고 자료 내용 생성
            docs = search_similar_documents(  
                vector_store,
                step["title"]
            )
            
            print("RAG DOC COUNT:", len(docs))

            # 검색된 문서 내용 연결
            context = "\n\n".join([
                doc.page_content
                for doc in docs
            ])
            print("===== RAG CONTEXT =====")
            print(context[:3000])
            print("=======================")
            
        #LangChain 템플릿에 값 넣음 , explain_chain 실행
        response = explain_chain.invoke({
            "category": category,
            "topic": topic,
            "step_number": step["step"],
            "step_title": step["title"],
            "level": level,
            "context": context
        })
        
        content = response.content.strip()
        content = content.replace("\\n", "\n")

        return {
            "type": "step_lecture",  
            # 커리큘럼의 한 단계를 가르치게 함
            # 프론트에서 구분하기 쉽게 하기 위해, type 은 화면을 어떻게 그릴지 결정하는 값이다.
            # "type": "explain"       → 그냥 질문에 답해주는 AI ,단발성 질문 답변
            # "type": "step_lecture" → 커리큘럼 안에서 가르치는 AI , 학습 과정 안의 한 단계
            
            "content": content
        }

    except Exception as e:
        
        print("EXPLAIN ERROR:", e)
        
        return {
            "type": "step_lecture",
            "content": "강의를 생성하는 중 문제가 발생했습니다. 다시 시도해주세요."
        }
        
#3. 현재 학습 흐름 기반 질문 답변
def generate_question_answer(category: str, topic: str, step: dict, level: str, question: str):

    try:
        # 질문 답변 전용 Chain 실행
        response = question_answer_chain.invoke({
            "category": category,
            "topic": topic,
            "step_number": step["step"],
            "step_title": step["title"],
            "level": level,
            "question": question
        })

        content = response.content.strip()
        content = content.replace("\\n", "\n")

        return {
            "type": "question_answer",
            "content": content
        }

    except Exception as e:

        return {
            "type": "question_answer",
            "content": (
                "질문 답변을 생성하는 중 문제가 발생했습니다. "
                "다시 시도해주세요."
            )
        }
        
#4. 현재 step 재설명(복습) 전용 함수
def generate_review_lecture(category: str, topic: str, step: dict, level: str):
    
    try:
        # 복습 전용 Chain 실행
        response = review_lecture_chain.invoke({
            "category": category,
            "topic": topic,
            "step_number": step["step"],
            "step_title": step["title"],
            "level": level
        })

        content = response.content.strip()
        content = content.replace("\\n", "\n")

        return {
            "type": "review_lecture",
            "content": content
        }

    except Exception as e:

        return {
            "type": "review_lecture",
            "content": (
                "복습 설명을 생성하는 중 문제가 발생했습니다. "
                "다시 시도해주세요."
            )
        }
        
#5. 현재 step 심화 설명(continue_learning) 전용 함수
def generate_continue_learning_lecture(category: str, topic: str, step: dict, level: str):

    try:
        # 심화 설명 전용 Chain 실행
        response = continue_learning_chain.invoke({
            "category": category,
            "topic": topic,
            "step_number": step["step"],
            "step_title": step["title"],
            "level": level
        })

        content = response.content.strip()
        content = content.replace("\\n", "\n")


        return {
            "type": "continue_learning_lecture",
            "content": content
        }

    except Exception as e:

        return {
            "type": "continue_learning_lecture",
            "content": (
                "심화 설명을 생성하는 중 문제가 발생했습니다. "
                "다시 시도해주세요."
            )
        }