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
def generate_step_lecture(category: str, topic: str, step: str, level: str, message, study_mode=None, vector_store=None):
    
    print("=== GENERATE STEP LECTURE RUNNING ===")
    
    # 학습 모드 제어 , 같은 강의 스타일을 유지하되 얼마나 깊게 설명할지(자유/가벼운 확인/집중 학습의 밀도 차이)
    
    if study_mode == "strict_quiz":
        mode_instruction = """
            현재 모드는 집중 학습 모드다.

            이 모드는 Study GPT에서 가장 밀도 높은 강의 모드다.

            중요한 것은 난이도를 무작정 높이는 것이 아니라,
            현재 학습 수준(level)과 현재 학습 단계(step)에 맞는 내용을
            가장 깊고 자세하게 설명하는 것이다.

            ----------------------------------------

            [매우 중요한 규칙]

            - 강의를 억지로 길게 작성하는 것이 목적은 아니다.
            - 그러나 짧은 요약이나 개념 나열로 끝내는 것은 절대 금지한다.
            - 사용자가 추가 질문을 하지 않아도 현재 step의 핵심을 충분히 이해할 수 있어야 한다.
            - 하나의 핵심 개념을 끝까지 이해시킨다는 느낌으로 강의하라.
            - 현재 step에서 가장 중요한 개념 1~2개를 중심으로 깊게 설명하라.

            ----------------------------------------

            [반드시 포함해야 하는 내용]

            - 왜 이 개념이 필요한가
            - 이 개념이 해결하는 문제는 무엇인가
            - 전체 학습 흐름 속에서 현재 개념은 어떤 역할을 하는가
            - 내부적으로 어떤 원리로 동작하는가
            - 기본 예시 (개념 이해용)
            - 실전형 예시 (실제 프로젝트·실제 작업 흐름 적용)
            - 사람들이 가장 많이 헷갈리는 부분
            - 다음 단계로 넘어가기 전에 반드시 이해해야 할 핵심 정리

            ----------------------------------------

            [설명 방식]

            - 단순 정의만 나열하지 마라.
            - 교과서식 개요 설명으로 끝내지 마라.
            - 압축 요약하지 마라.
            - 사용자가 자연스럽게 사고 흐름을 따라갈 수 있도록 설명하라.

            - 하나의 개념을 설명할 때는 반드시

            "왜 생겨났는가
            ↓
            어떤 문제를 해결하는가
            ↓
            실제로 어떻게 사용하는가
            ↓
            내부적으로 어떤 원리로 동작하는가"

            의 흐름으로 설명하라.

            - 쉬운 표현은 유지하되 설명의 밀도는 높게 유지하라.
            - 현재 level이 초급이어도 설명량을 과하게 줄이지 마라.
            - 초급은 쉬운 언어로 깊게 설명하고,
            중급·고급은 구조와 원리까지 더욱 깊게 설명하라.

            ----------------------------------------

            [코드 관련 주제]

            코드를 설명하는 경우에는

            - 문법 설명에서 끝내지 마라.
            - 코드가 프로그램 전체 구조에서 어떤 역할을 하는지 설명하라.
            - 왜 이런 구조로 작성하는지 설명하라.
            - 실제 프로젝트에서는 어떻게 사용하는지 설명하라.

            기본 예시와 실전형 예시는 반드시 구분하여 작성한다.

            기본 예시는
            → 개념 자체를 이해시키기 위한 예시

            실전형 예시는
            → 실제 프로젝트, 유지보수, 역할 분리, 작업 흐름 중 하나 이상을 반드시 포함한다.

            ----------------------------------------

            [비코드 주제]

            비코드 주제를 설명하는 경우에는

            - 실제 적용 사례
            - 실제 업무 흐름
            - 실제 판단 과정
            - 현장에서 활용되는 방식

            중 하나 이상을 반드시 포함하여 설명하라.

            ----------------------------------------

            [강의 스타일]

            - 사용자가 AI 답변을 읽는 느낌이 아니라
            실제 강의를 듣는 느낌이 들도록 설명하라.

            - 중간중간
            "왜 그럴까?"
            "여기서 중요한 점은..."
            "많은 사람들이 여기서 헷갈린다."
            와 같은 자연스러운 강의식 흐름을 사용하라.

            - 단순히 정보를 전달하는 것이 아니라,
            사용자가 개념을 이해하도록 가르치는 것이 목적이다.

            ----------------------------------------

            [마무리]

            마지막은 단순 요약으로 끝내지 마라.

            반드시

            "다음 단계로 넘어가기 전에 반드시 이해해야 하는 체크리스트"

            형태로 마무리하라.
            """

    elif study_mode == "light_quiz":
        mode_instruction = """
        현재 모드는 가벼운 확인 모드다.

        이 모드는 짧은 설명 모드가 아니다.
        사용자가 강의를 충분히 이해한 뒤, 원하면 확인용 퀴즈를 풀 수 있도록 핵심을 선명하게 정리하는 모드다.

        매우 중요:
        - 설명을 5~10줄로 짧게 끝내지 마라.
        - 자유 학습보다 구조적으로 설명하라.
        - 집중 학습보다 과도한 심화는 줄이되, 강의 품질은 유지하라.
        - 퀴즈는 자동으로 강제하지 마라.

        반드시 포함해야 한다:
        - 이 개념이 왜 필요한가
        - 핵심 개념 설명
        - 쉬운 예시
        - 실제 사용 흐름
        - 많이 헷갈리는 부분
        - 확인하면 좋은 핵심 포인트

        설명 방식:
        - 사용자가 바로 이해 확인을 할 수 있게 핵심을 분명히 정리하라
        - 너무 얕은 요약으로 끝내지 마라
        - 개념의 흐름은 충분히 설명하라
        - 마지막에는 퀴즈를 강제하지 말고, 확인 포인트만 자연스럽게 남겨라
        """

    else:
        mode_instruction = """
        현재 모드는 자유 학습 모드다.

        이 모드는 사용자가 부담 없이 학습을 이어가는 모드다.
        하지만 짧고 얕은 답변 모드가 아니다.

        매우 중요:
        - 설명 품질을 낮추지 마라.
        - 사이드챗처럼 짧은 답변으로 끝내지 마라.
        - 현재 step을 이해할 수 있을 만큼 충분히 설명하라.
        - 퀴즈나 다음 단계 진행을 강하게 유도하지 마라.

        반드시 포함해야 한다:
        - 이 개념이 왜 필요한가
        - 핵심 개념 설명
        - 쉬운 예시
        - 헷갈리기 쉬운 부분
        - 핵심 정리

        설명 방식:
        - 자연스럽고 부담 없는 튜터 말투를 사용하라
        - 사용자가 자유롭게 질문을 이어갈 수 있게 마무리하라
        - 너무 딱딱한 강의체보다 편안한 설명 흐름을 유지하라
        """
    
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
            "study_mode": study_mode,
            "mode_instruction": mode_instruction,
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