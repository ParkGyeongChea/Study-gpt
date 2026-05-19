#quiz_service.py

from services.session_service import get_study_session
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


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
    

    #4.prompt 작성
    prompt = f"""
        너는 초보자를 위한 학습 퀴즈를 만들어주는 AI다.

        현재 학습 정보:

        - 카테고리: {category}
        - 주제: {topic}
        - 현재 학습 단계: {step_title}
        - 난이도: {level}

        규칙:

        - 현재 학습 단계(step_title) 중심으로 문제를 만들어라
        - 초보자도 이해할 수 있게 쉽게 만들어라
        - 객관식 문제만 생성하라
        - 문제는 1~2개만 생성하라
        - 각 문제의 보기는 4개로 구성하라
        - 정답도 함께 출력하라
        - 너무 길게 설명하지 마라

        출력 형식 예시:

        Q1.
        1.
        2.
        3.
        4.

        정답:

        Q2.
        1.
        2.
        3.
        4.

        정답:
    """

    
    try:

        response = llm.invoke(prompt)
        # ChatOpenAI()로 생성한 GPT 객체 llm을 이용해서,
        # 현재 작성한 prompt를 GPT에게 보내고 응답을 받아오는 코드

        quiz_content = response.content.strip()
        # llm.invoke(prompt)로 받아온 GPT 응답 객체(response) 안에서,
        # 실제 텍스트(content)만 꺼내고,
        # strip()으로 앞뒤 공백 제거

        return quiz_content
        # 최종 퀴즈 문자열 반환


    except Exception as e:

        print("quiz error:", e)
        # 실제 에러 내용을 콘솔에 출력
        # 디버깅(오류 확인)용

        return "퀴즈 생성 중 오류가 발생했습니다."
        # 사용자에게 반환할 오류 메시지