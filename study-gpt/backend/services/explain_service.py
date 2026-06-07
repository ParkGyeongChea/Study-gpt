#explain_service.py

from services.shared_llm import llm 
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
 
    
    try:
        #랭체인 프롬프트 호출
        response = explain_chat_chain.invoke({
            "message": message
        })
        
        content = response.content.strip()
        content = content.replace("\\n", "\n")

        return { 
            "type": "explain", 
            "content": content 
        }

    except Exception as e: 
        return { 
            "type": "explain",
            "content": "설명을 생성하는 중 문제가 발생했습니다. 다시 시도해주세요."
        }
        
        
#2. 커리큘럼 단계 강의용 함수 생성
def generate_step_lecture(category: str, topic: str, step: str, level: str, message, vector_store=None):
    
    print("=== GENERATE STEP LECTURE RUNNING ===")
    
    try:
        
        # 기본 context
        context = "참고 자료 없음"

        # RAG 문서 검색
        if vector_store:
            
            print("VECTOR STORE EXISTS")
            print("MESSAGE:", message)
            print("TOPIC:", topic)
            
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