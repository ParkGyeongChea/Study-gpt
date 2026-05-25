#quiz_service.py
#퀴즈 실제 데이터 전달, 응답 후처리, json 파싱

from services.session_service import get_study_session
from langchain_openai import ChatOpenAI
from services.chains.quiz_chain import quiz_chain
from dotenv import load_dotenv
import json


# .env 파일 환경변수 로드
load_dotenv()


#gpt객체
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.5
)


# 퀴즈 생성 함수
# db에서 현재 로그인 사용자 기준 학습 상태를 가져옴
def generate_quiz(db, user_id: int, room_id: int):
    
    #1.현재 학습 상태 가져오기
    session = get_study_session(db, user_id, room_id)
    # session_service.py 파일에서,
    # 현재 학습 상태를 반환하는 역할을 하는
    # get_study_session() 함수 실행
    # 현재 로그인 사용자의 studySession DB 데이터 조회
    
    # 사용자가 학습 시작을 하지 않고 바로 퀴즈 요청 하는 경우 
    if session is None:

        return "먼저 학습을 시작해주세요."
    

    #2.StudySession ORM 객체에서 필요한 값 가져오기
    #(이전) .get 은 딕셔너리 값을 가져옴, session.값은 orm 객체 속성 접근
    category = session.category
    topic = session.topic
    level = session.level
    current_step = session.current_step
    

    #3.current_step(dict 형태 step 객체) 안에서
    # 현재 단계 제목(title)만 꺼내기
    step_title = current_step.get("title")
    

    #chain 연결
    try:
        response = quiz_chain.invoke({
            "category": category,
            "topic": topic,
            "step_title": step_title,
            "level": level
        })

        quiz_content = response.content.strip()
        # llm.invoke(prompt)로 받아온 GPT 응답 객체(response) 안에서,
        # 실제 텍스트(content)만 꺼내고,
        # strip()으로 앞뒤 공백 제거
        
        # GPT JSON 문자열 → Python dict 변환
        quiz_data = json.loads(quiz_content)

        # 사용자에게 보여줄 퀴즈 데이터
        quiz_for_user = []
        for quiz in quiz_data["quiz"]:
            #quiz_for_user = 사용자 화면 전용 데이터
            quiz_for_user.append({
                "question": quiz["question"],
                "choices": quiz["choices"]
            })

        # 내부 정답 데이터 포함 반환
        return {
            "quiz_for_user": quiz_for_user,
            "quiz_answer_data": quiz_data["quiz"]
        }


    except Exception as e:

        print("quiz error:", e)
        # 실제 에러 내용을 콘솔에 출력
        # 디버깅(오류 확인)용

        return "퀴즈 생성 중 오류가 발생했습니다."
        # 사용자에게 반환할 오류 메시지