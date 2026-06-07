# agent_service.py

# 역할
# message 입력 -> intent 분석 -> 기능 분기 -> 결과 반환
# 사용자 입력을 가장 먼저 판단하는 중앙 제어 서비스 파일
# 현재는 JWT 인증으로 확인된 user_id와 DB 연결(db)을 함께 받아서
# 사용자별 학습 상태를 DB 기준으로 조회/수정한다.

from services.llm_service import analyze_intent
from services.explain_service import (explain_service,generate_step_lecture)
from services.session_service import (get_study_session,update_step_index,update_current_step)
from services.chains.document_intent_chain import analyze_document_intent
from services.chat_message_service import save_chat_message
from services.room_service import (generate_room_title, update_room_title) 
from services.chat_message_service import get_chat_messages 
from services.chat_service import chat_service
from services.quiz_service import generate_quiz
from services.session_service import save_study_session
from services.rag_service import (
    load_pdf,
    load_txt,
    split_documents,
    create_vector_store,
    save_local_vector_store, 
    load_local_vector_store, 
    add_documents_to_vector_store,
    search_similar_documents
)
from services.chains.document_curriculum_chain import (
    generate_document_curriculum 
)

from services.curriculum_service import (
    parse_curriculum 
)

from services.graph.study_graph import app as study_graph_app
from services.graph.learning_flow_graph import app as learning_flow_app
from services.chains.learning_intent_chain import (learning_intent_chain)
from services.vector_store_manager import (save_vector_store,get_vector_store)

import json
import os
from fastapi import UploadFile

#===================================================================

# 1. 사용자 입력을 가장 먼저 받아서, 무슨 기능을 실행할지 판단하는 중앙 제어 함수.
def run(db, user_id: int, room_id: int, message: str, study_mode: str = None, files: list[UploadFile] | None = None):
    
    messages = []
    
    # 업로드 파일 저장 처리
    uploaded_file_paths = []

    if files:

        # uploads 폴더 자동 생성
        os.makedirs("uploads",exist_ok=True)

        for file in files:

            # 저장 경로 생성
            file_path = (f"uploads/{file.filename}")

            # 실제 파일 저장
            with open(
                file_path,
                "wb"
            ) as buffer:

                buffer.write(
                    file.file.read()
                )

            uploaded_file_paths.append(
                file_path
            )

        print("업로드 파일:",uploaded_file_paths)
        
        
        # 업로드 PDF 문서 읽기
        uploaded_documents = []

        for file_path in uploaded_file_paths:

            try:
                # 파일 확장자 확인
                file_extension = os.path.splitext(file_path)[1].lower()

                # PDF 문서 로드
                if file_extension == ".pdf":
                    documents = load_pdf(file_path)

                # TXT 문서 로드
                elif file_extension == ".txt":
                    documents = load_txt(file_path)

                # 지원하지 않는 파일 형식
                else:
                    print(f"지원하지 않는 파일 형식입니다: {file_path}")
                    continue

                uploaded_documents.extend(documents)
                print(f"문서 로드 완료: {file_path}")
                      
                # 업로드 문서 chunk 분리
                vector_store = None

                if uploaded_documents:

                    # chunk 분리
                    split_docs = split_documents(uploaded_documents)

                    print(f"chunk 생성 완료: {len(split_docs)}개")

                    # 기존 vector_store 존재 시 새 문서 merge
                    if vector_store:

                        vector_store = (
                            add_documents_to_vector_store(vector_store,split_docs)
                        )

                        print("기존 VECTOR STORE 문서 merge 완료")

                    # 기존 vector_store 없으면 새 생성
                    else:
                        vector_store = (create_vector_store(split_docs))

                        print("새 VECTOR STORE 생성 완료")
                    
                    # 디스크에도 저장
                    if room_id:
                        save_local_vector_store(vector_store, room_id)
                                        
                    # room 기준 vector_store 저장
                    if room_id:

                        save_vector_store(room_id,vector_store)
                        print(f"VECTOR STORE 저장 완료: room {room_id}")

            except Exception as e:
                print(f"문서 로드 실패: {e}")
 
    # 기존 vector_store 복구

    vector_store = None

    if room_id:

        # 1. RAM 메모리에서 먼저 조회
        vector_store = get_vector_store(room_id)

        if vector_store:

            print(f"기존 VECTOR STORE 복구 완료: room {room_id}")

        # 2. RAM에 없으면 디스크에서 복구 시도
        if not vector_store:

            vector_store = load_local_vector_store(room_id)

            # 3. 디스크 복구 성공 시 RAM에도 다시 저장
            if vector_store:

                save_vector_store(
                    room_id,
                    vector_store
                )

                print(f"디스크 VECTOR STORE RAM 복구 완료: room {room_id}")

    # 로그인 사용자일 때만 기존 메시지 조회
    if user_id and room_id:

        messages = get_chat_messages(db, room_id)
        
    
    # 로그인 사용자이고, room_id가 있고 첫 메시지일 때만 채팅방 제목 자동 생성.
    if user_id and room_id and len(messages) == 0:
        
        #사용자 첫 메시지 기반 제목 생성 , gpt에게 제목 생성 요청
        new_title = generate_room_title(message)
        
        #실제 DB room 제목 수정
        update_room_title(db, room_id, user_id, new_title)
   
    
    # 로그인 사용자일 때만 메시지 저장
    if user_id and room_id:

        save_chat_message(
            db,
            user_id,
            room_id,
            "user",
            message
        )
    
    # 강의 재요청 처리 현재 학습 단계 반복 학습 가능 함수
   
    if (
        (
            "다시 설명" in message
            or "모르겠어" in message
            or "이해 안돼" in message
            or "설명 다시" in message
        )
        and "문제" not in message
        and "퀴즈" not in message
    ):
        
        #임시 에러 대비 코드 추후에 삭제or변경
        if not user_id or not room_id:
            return {
                "lecture": {
                    "content": "로그인 후 학습 기록을 저장하면 다시 설명 기능을 사용할 수 있습니다."
                }
            }

        #현재 로그인 사용자의 학습 상태 가져오기
        # session_service.py 파일(사용자 학습 상태를 DB에서 조회하는 역할)의 get_study_session 함수 호출 
        session = get_study_session(db,user_id,room_id)
        

        # 학습 상태 존재 여부 예외처리 검사 
        if session is None:
            # DB에 저장된 학습 상태가 없으면 다시 설명할 현재 단계도 없음
            return {
                "message": "먼저 학습하고 싶은 내용을 알려주세요."
            }

        # 현재 저장된 학습 상태 가져오기
        curriculum = session.curriculum
        
        # DB에 저장된 현재 학습 단계 index 가져오기
        current_step_index = session.current_step_index
        
        # 현재 사용자가 배우고 있는 step 데이터 가져오기
        current_step = curriculum[current_step_index]
        

        # learning_flow_graph 실행용 state 생성
        learning_state = {
            "message": message,
            "intent": "study",
            "category": session.category,
            "topic": session.topic,
            "level": session.level,
            "curriculum": curriculum,
            "current_step": current_step,
            "response": {},
            "learning_intent": "",
            "user_id": user_id,
            "room_id": room_id,
            "db": db,
            "learning_status": session.learning_status,
            "vector_store": vector_store
            
        }
        
        # learning_flow_graph 실행
        learning_result = learning_flow_app.invoke(
            learning_state
        )

        # Graph 생성 강의 결과 가져오기
        lecture = learning_result["response"]
        

        # lecture가 dict 구조인 경우
        if isinstance(lecture, dict):

            lecture_content = lecture["content"]

        
        else:

            lecture_content = lecture

        # 로그인 사용자에 한해서만 AI 강의 응답 저장
        if user_id and room_id:

            save_chat_message(
                db,
                user_id,
                room_id,
                "assistant",
                lecture_content
            )

        #progress(학습 진행도) 기능

        total_steps = len(curriculum)
        # 전체 커리큘럼 단계 수 계산

        current_step_number = current_step_index + 1
        # 현재 단계 번호 계산
        # index는 0부터 시작하므로 사용자 표시용으로 +1

        progress_percent = int((current_step_number / total_steps) * 100)
        # 진행률 퍼센트 계산

        # 반환
        return {
            "type": "lecture",
            "current_step": current_step,

            "lecture": {
                "content": lecture_content
            },
            "progress": {
                "current": current_step_number,
                "total": total_steps,
                "percent": progress_percent
            }
        }
        
    # 비로그인 사용자는 DB 기반 학습 시스템으로 보내지 않고 임시 체험 응답을 바로 반환
    if not user_id or not room_id:

        return {
                "lecture": {
                    "content": """
            🔒 비로그인 상태입니다.

            Study GPT의 AI 학습 기능은 로그인 후 사용할 수 있습니다.

            로그인하면 다음 기능을 사용할 수 있습니다.

            - 학습 기록 저장
            - 채팅방 저장
            - 이어서 학습
            """
                }
            }
        
    # 현재 로그인 사용자의 학습 세션 조회
    session = get_study_session(db, user_id, room_id)
    

    # 학습 일시정지 상태 검사
   
    if session and session.learning_status == "paused":

        # 사용자가 학습 재개 의도를 보낸 경우
        resume_keywords = [
            "다시 시작",
            "다시시작",
            "학습 다시 시작",
            "이어",
            "이어서",
            "이어할게",
            "이어할래",
            "계속할게",
            "계속",
            "재개",
            "다시 할게"
        ]

        if any(keyword in message for keyword in resume_keywords):

            # 학습 상태 복구
            session.learning_status = "learning"

            db.commit()
            db.refresh(session)
            
            # 현재 step 강의 다시 생성
            lecture = generate_step_lecture(
                category=session.category,
                topic=session.topic,
                step=session.current_step,
                level=session.level,
                message=message
            )

            # lecture가 dict 구조인 경우
            if isinstance(lecture, dict):

                lecture_content = lecture["content"]

            # 문자열인 경우
            else:

                lecture_content = lecture

            save_chat_message(
                db,
                user_id,
                room_id,
                "assistant",
                lecture_content
            )

            return {
                "message": "학습을 다시 시작합니다. 이전 학습 단계부터 이어서 진행할게요!",
                "current_step": session.current_step,

                "lecture": {
                    "content": lecture_content
                }
            }

        # 아직 재개 요청이 아닌 경우
        return {
            "message": (
                "현재 학습이 일시정지 상태입니다.\n\n"
                "학습을 다시 시작하려면:\n"
                "- 다시 시작할게\n"
                "- 이어서 할게\n"
                "- 학습 재개\n\n"
                "처럼 입력해주세요!."
            )
        }
        
    
    # learning intent 분석
    learning_intent = None

    # 현재 학습 session 존재 시에만 실행
    if session:

        current_step_title = session.current_step.get("title", "")

        learning_response = (
            learning_intent_chain.invoke({
                "message": message,
                "current_step": current_step_title
            })
        )

        learning_intent = (
            learning_response.content.strip()
        )
        
        print("learning_intent:", learning_intent)
    
    # 현재 퀴즈 진행 중인지 확인
    if session and session.quiz_answer_data:
        
        if (
            message.strip() in ["다음", "다음 단계", "계속"]
            or learning_intent == "next_step"
        ):
            pass
        else:
            # 사용자 입력 답안 분리
            user_answers = [
                answer.strip()
                for answer in message.split(",")
            ]

            quizzes = session.quiz_answer_data
            result_messages = []

            for index, quiz in enumerate(quizzes):
                correct_answer = quiz["answer"]
                explanation = quiz["explanation"]

                # 사용자가 답을 덜 입력한 경우
                if index >= len(user_answers):
                    result_messages.append(
                        f"❌ Q{index + 1} 답변이 입력되지 않았습니다."
                    )
                    continue

                user_answer = user_answers[index]

                # 정답 판별
                if user_answer == correct_answer:
                    result_messages.append(
                        f"✅ Q{index + 1} 정답입니다!"
                    )

                else:
                    result_messages.append(
                        f"❌ Q{index + 1} 틀렸습니다.\n\n"
                        f"📘 해설:\n{explanation}"
                    )
            # 최종 해설 메시지 생성
            quiz_result_message = (
                "\n\n---\n\n".join(result_messages)
            )

            # 퀴즈 상태 초기화
            session.quiz_answer_data = None

            db.commit()

            
            # 퀴즈 결과 메시지 DB 저장
            if user_id and room_id:

                save_chat_message(
                    db,
                    user_id,
                    room_id,
                    "assistant",
                    json.dumps({
                        "type": "quiz_result",
                        "content": quiz_result_message
                    }, ensure_ascii=False)
                )

            # 사용자 응답 반환
            return {

                "type": "quiz_result",

                "message": quiz_result_message

            }


    # 다음 단계 요청 처리
    if (
        message.strip() in ["다음", "다음 단계", "계속"]
        or learning_intent == "next_step"
    ):
        
        if not user_id or not room_id:
            return {
                "lecture": {
                    "content": "로그인 후 학습 기록을 저장하면 다음 단계 기능을 사용할 수 있습니다."
                }
            }
            
       
        # 현재 로그인 사용자의 학습 상태 가져오기
        session = get_study_session(db, user_id, room_id)
        
        # 학습 상태 존재 여부 예외처리 검사
        if session is None:
            
            return {
                "message": "먼저 학습하고 싶은 내용을 알려주세요."
            }
            
        # learning_flow_graph 실행용 state 생성
        # 현재 DB에 저장된 학습 상태를 기반으로 learning_flow_graph 실행 준비
        learning_state = {
            "message": message,
            "intent": "study",
            "category": session.category,
            "topic": session.topic,
            "level": session.level,
            "curriculum": session.curriculum,
            "current_step": session.current_step,
            "response": {},
            "learning_intent": "",
            "user_id": user_id,
            "room_id": room_id,
            "db": db,
            "learning_status": session.learning_status,
            "vector_store": vector_store
        }
        
        # learning_flow_graph 실행
        learning_result = learning_flow_app.invoke(learning_state)
        
        print(learning_result)

        # Graph 결과에서 새 현재 step 가져오기
        new_current_step = learning_result["current_step"]

        # Graph 결과에서 새 강의 가져오기
        lecture = learning_result["response"]


        # 현재 step 완료 처리
        current_step_index = session.current_step_index

        session.curriculum[current_step_index]["completed"] = True


        # 새로운 step index 계산
        new_index = new_current_step["step"] - 1


        # DB 현재 step 저장
        update_step_index(
            db,
            user_id,
            room_id,
            new_index
        )

        update_current_step(
            db,
            user_id,
            room_id,
            new_current_step
        )


        #progress 계산
        total_steps = len(session.curriculum)

        current_step_number = new_current_step["step"]

        progress_percent = int(
            (current_step_number / total_steps) * 100
        )

        session.progress = progress_percent
        db.commit()
        db.refresh(session)

        #AI 강의 저장 
        if user_id and room_id:

            save_chat_message(
                db,
                user_id,
                room_id,
                "assistant",
                lecture["content"]
            )

        # Graph 기반 응답 반환
        return {
            "type": "lecture",
            "current_step": new_current_step,
            "lecture": lecture,
            "progress": {
                "current": current_step_number,
                "total": total_steps,
                "percent": progress_percent
            }
        }
    
    # learning_intent 기반 graph 처리
    
    if learning_intent in [
        "pause_learning",
        "finish_learning",
        "review",
        "continue_learning",
        "unknown_intent"
    ]:
        learning_state = {
            "message": message,
            "intent": "study",
            "category": session.category,
            "topic": session.topic,
            "level": session.level,
            "curriculum": session.curriculum,
            "current_step": session.current_step,
            "response": {},
            "learning_intent": learning_intent,
            "user_id": user_id,
            "room_id": room_id,
            "db": db,
            "learning_status": session.learning_status,
            "vector_store": vector_store
        }

        # learning_flow_graph 실행
        learning_result = (
            learning_flow_app.invoke(
                learning_state
            )
        )

        response_message = learning_result["response"]

        # response가 dict 구조인 경우
        if isinstance(response_message, dict):

            message_content = response_message["content"]

        # 문자열인 경우
        else:
            message_content = response_message
            
        # AI 응답 저장
        if user_id and room_id:

            save_chat_message(
                db,
                user_id,
                room_id,
                "assistant",
                message_content
            )

        # dict 응답이면 그대로 반환
        if isinstance(response_message, dict):

            return {
                "type": "lecture",
                "lecture": response_message
            }

        # 문자열 응답이면 lecture 구조로 감싸기
        return {
            "lecture": {
                "content": response_message
            }
        }
    

    intent = analyze_intent(message)
    # llm_service.py 파일(사용자 입력 의도 분석 역할)의 analyze_intent 함수 호출
    # study / explain / quiz / chat 중 어떤 요청인지 판단한다.
    
    
    # 업로드 문서 존재 시
    # document intent 분석 우선 처리
    if vector_store:

        intent = analyze_document_intent(message)

        print("DOCUMENT RAG MODE ENABLED")


    print("intent:", intent)
    
    
    # document_chat 요청 업로드 문서 기반 RAG 응답
    
    if intent == "document_chat":

        document_state = {
            "message": message,
            "intent": "document_chat",
            "category": "",
            "topic": "",
            "level": "",
            "curriculum": [],
            "current_step": {},
            "response": {},
            "learning_intent": "document_chat",
            "vector_store": vector_store,
            "user_id": user_id,
            "room_id": room_id,
            "db": db,
            "learning_status": ""
        }

        document_result = learning_flow_app.invoke(document_state)

        response = document_result["response"]

        if user_id and room_id:
            save_chat_message(
                db,
                user_id,
                room_id,
                "assistant",
                response["content"]
            )

        return {
            "type": "document_chat",
            "lecture": {
                "content": response["content"]
            }
        }
    
    # document_study 요청 문서 기반 AI 학습 시작
    
    if intent == "document_study":

        print("DOCUMENT STUDY MODE")

        # 문서 retrieval
        related_docs = search_similar_documents(
            vector_store,
            message
        )

        # retrieval text 합치기
        context = "\n\n".join([
            doc.page_content
            for doc in related_docs
        ])

        print("===== DOCUMENT CURRICULUM CONTEXT =====")
        print(context)
        print("======================================")

        # 문서 기반 curriculum 생성
        curriculum_text = (
            generate_document_curriculum(
                context
            )
        )

        print("===== DOCUMENT CURRICULUM =====")
        print(curriculum_text)
        print("================================")

        # 기존 curriculum 구조 변환
        curriculum = parse_curriculum(
            curriculum_text
        )

        # 첫 step 설정
        current_step_index = 0

        current_step = curriculum[
            current_step_index
        ]

        

        # 문서 기반 첫 step 강의 직접 생성
        response = generate_step_lecture(
            category="문서 기반 학습",
            topic=current_step["title"],
            step=current_step,
            level="초급",
            message=message,
            vector_store=vector_store
        )

        response_content = response["content"]

        
        # 학습 세션 저장
        save_study_session(
            db=db,
            user_id=user_id,
            room_id=room_id,
            category="문서 기반 학습",
            topic=current_step["title"],
            level="초급",
            curriculum=curriculum,
            current_step_index=0,
            current_step=current_step,
            study_mode=study_mode,
            learning_status="learning"
        )

        # AI 응답 저장
        save_chat_message(
            db,
            user_id,
            room_id,
            "assistant",
            response_content
        )

        return {
            "type": "document_study",

            "current_step": current_step,

            "lecture": response,

            "progress": {
                "current": 1,
                "total": len(curriculum),
                "percent": int((1 / len(curriculum)) * 100)
            }
        }
        
    

    
    # study 요청
    
    if intent == "study":
        if study_mode is None:
            # 사용자가 공부 요청은 했지만 아직 학습 모드를 선택하지 않은 경우
            # 바로 학습을 시작하지 않고, 프론트에 모드 선택 UI를 띄울 수 있는 응답을 반환한다.

            return {
                "type": "mode_select",
                "message": "어떤 학습 모드로 진행할까요?",
                "modes": [
                    {
                        "id": "free",
                        "title": "자유 학습 모드",
                        "description": "퀴즈 없이 강의 중심으로 학습합니다."
                    },
                    {
                        "id": "light_quiz",
                        "title": "가벼운 확인 모드",
                        "description": "각 챕터가 끝난 뒤 간단한 문제를 제공합니다."
                    },
                    {
                        "id": "strict_quiz",
                        "title": "집중 학습 모드",
                        "description": "문제를 통과해야 다음 단계로 진행 가능합니다."
                    }
                ]
            }
            
        # 학습 시작 처리  
        # LangGraph 실행용 초기 state 생성
        initial_state = {
            "message": message,
            "intent": intent,
            "category": "",
            "topic": "",
            "level": "",
            "curriculum": [],
            "current_step": {},
            "response": {},
            "learning_intent": "",
            "vector_store": vector_store
        }
        
        # study_graph 실행
        graph_result = study_graph_app.invoke(initial_state)
        
        print(graph_result)
        
        # Graph 결과 데이터 꺼내기 , GraphState 안에 저장된 결과들을 실제 서비스에서 사용 가능하게 꺼내는 단계
        category = graph_result["category"]
        topic = graph_result["topic"]
        level = graph_result["level"]
        curriculum = graph_result["curriculum"]
        current_step = graph_result["current_step"]
        response = graph_result["response"]
        
        if isinstance(response, str):
            response = {
                "type": "step_lecture",
                "content": response
            }
        
        # Graph 결과 기반 학습 상태 저장
        save_study_session(
            db=db,
            user_id=user_id,
            room_id=room_id,
            category=category,
            topic=topic,
            level=level,
            curriculum=curriculum,
            current_step_index=0,
            current_step=current_step,
            study_mode=study_mode,
            learning_status="learning"
        )
        
        # Graph 생성 강의 DB 저장
        if user_id and room_id:

            save_chat_message(
                db,
                user_id,
                room_id,
                "assistant",
                response["content"]
            )
        
                
        # Graph 기반 응답 구조 생성
        graph_study_result = {
            "type": "lecture",
            "current_step": current_step,
            "lecture": response,
            "progress": {
                "current": 1,
                "total": len(curriculum),
                "percent": int((1 / len(curriculum)) * 100)
            }
        }
        print(graph_study_result)
                
        return graph_study_result
    
    

    # explain 요청
    elif intent == "explain":

        response = explain_service(message)
        
        #사용자가 로그인 했을 시에만 아래 데이터 저장
        if user_id and room_id:
            save_chat_message(
                db,
                user_id,
                room_id,
                "assistant",
                response["content"]
            )

        return {
            "type": "lecture",
            "lecture": response
        }


    # quiz 요청
    elif intent == "quiz":

        # 학습 session 없는 경우
        if not session:
            return {
                "type": "info",
                "lecture": {
                    "content":
                    "현재 진행 중인 학습이 없습니다.\n\n"
                    "먼저 학습을 시작해주세요!"
                }
            }

        # 현재 step 기준 퀴즈 생성
        quiz_result = generate_quiz(
            category=session.category,
            topic=session.topic,
            step=session.current_step,
            level=session.level
        )

        # 퀴즈 생성 실패 예외 처리
        if isinstance(quiz_result, str):

            return {
                "type": "info",
                "lecture": {
                    "content": quiz_result
                }
            }

        # 정답 데이터 DB 저장
        session.quiz_answer_data = (
            quiz_result["quiz_answer_data"]
        )

        db.commit()
        
        # 퀴즈 메시지 DB 저장
        if user_id and room_id:

            save_chat_message(
                db,
                user_id,
                room_id,
                "assistant",
                json.dumps({
                    "type": "quiz",
                    "quiz": quiz_result["quiz_for_user"]
                }, ensure_ascii=False)
            )
                
        
        # 사용자용 퀴즈 반환
        return {
            "type": "quiz",
            "quiz": quiz_result["quiz_for_user"]
        }

    # 일반 대화
    else:
        response = chat_service(message)
        
        #사용자가 로그인 했을 시에만 아래 데이터 저장
        if user_id and room_id:
            save_chat_message(
                db,
                user_id,
                room_id,
                "assistant",
                response["content"]
            )
        
        return {
            "lecture": {
                "content": response["content"]
            }
        }