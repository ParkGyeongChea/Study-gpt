#curriculum_service.py

# study_router.py가 받은 요청을 넘겨주면,
# curriculum_service.py가 그 요청을 해석해서
# 카테고리와 커리큘럼 결과를 만들어주는 파일
# 처리 담당

# curriculum_service.py

from services.llm_service import generate_curriculum

curriculum_map = {
    "영어": {
        "keywords": ["영어", "english", "회화", "영문", "토익", "토플"],
        "curriculum": [
            "알파벳",
            "기초 단어",
            "기초 문장",
            "기초 문법",
            "간단한 회화",
            "리스닝 연습",
            "독해 기초"
        ]
    },

    "수학": {
        "keywords": ["수학", "math", "계산", "방정식", "함수", "미적분"],
        "curriculum": [
            "숫자와 연산",
            "사칙연산",
            "분수와 소수",
            "방정식 기초",
            "함수 개념",
            "그래프 이해",
            "기초 미적분"
        ]
    },

    "코딩": {
        "keywords": ["코딩", "프로그래밍", "python", "파이썬", "개발"],
        "curriculum": [
            "변수",
            "조건문",
            "반복문",
            "함수",
            "리스트/딕셔너리",
            "간단한 프로젝트"
        ]
    },

    "FastAPI": {
        "keywords": ["fastapi", "api", "백엔드 api"],
        "curriculum": [
            "라우터 개념",
            "GET/POST 요청",
            "CRUD 구현",
            "의존성 주입",
            "DB 연결"
        ]
    },

    "백엔드": {
        "keywords": ["backend", "백엔드", "서버", "api 서버"],
        "curriculum": [
            "서버 개념",
            "API 구조",
            "데이터 흐름",
            "LangChain 기초",
            "LangGraph 기초"
        ]
    },

    "프론트엔드": {
        "keywords": ["frontend", "프론트엔드", "ui", "react"],
        "curriculum": [
            "HTML 기초",
            "CSS 기초",
            "JavaScript 기초",
            "React 구조",
            "상태 관리"
        ]
    }
}



def start_study_service(message: str): #사용자가 입력한 message
    
    message = message.lower().strip() 
    #사용자가 입력한 문장을 전부 소문자로 변환, 앞뒤 공백 제거.
    #이 코드를 아래 반복문에 넣으면, 불필요하게 계속 실행되니, 함수 시작과 동시에 실행하도록 함.
    #이 코드는 데이터 전처리 과정.

    
    category = None #처음에는 어떤 과목인지 모르니 None
    curriculum = None
    found = False
    
    # 1. 학습 수준(level) 기본값 설정
    level = "초급"

    if "중학생" in message or "중급" in message:
        level = "중급"
    elif "고등학생" in message:
        level = "중급"
    elif "대학교" in message or "고급" in message:
        level = "고급"

    # 2. 단계 수(step_count) 결정
    if level == "초급":
        step_count = 5
    elif level == "중급":
        step_count = 6
    else:
        step_count = 7

    # 디버깅용 출력
    print("DEBUG message:", message)
    print("DEBUG level:", level)
    print("DEBUG step_count:", step_count)

    # 3. 과목 찾기
    for subject in curriculum_map: #curriculum_map의 모든 과목을 하나씩 확인
        
        for keyword in curriculum_map[subject]["keywords"]: #해당 과목의 keywords 리스트를 하나씩 꺼냄 (2중 for문)
            
            if keyword in message: #사용자가 입력한 문장에 해당 과목(keywords)이 있는지 확인
                
                category = subject #해당  keyword가 포함되어 있으면 이 과목이 정답이므로 category에 저장
                
                curriculum = generate_curriculum(category, level, step_count) #llm_service의 해당 과목의 커리큘럼을 가져와서 저장
                
                found = True #과목을 찾았기 때문에 , found를 True 로 변경.
                
                break #keyword 반복문(안쪽 for문) 종료.
            
        if found: #과목을 이미 찾았다면
            break #바깥쪽 for문 (subject 반복) 도 종료.

    # 4. 못 찾은 경우 (에러 처리) 
    if category is None: #끝까지 돌았는데도 과목을 못찾음(None). 아래 에러 메시지 출력
        return {
            "error": "어떤 과목인지 이해하지 못했어요.",
            "message": "다시 한번 입력해주세요"
        }

    # 5. 정상 처리 
    #과목을 찾음. if문 밖, for문에 대한 return
    return {
        "category": category,
        "curriculum": curriculum
    }
    

    
    #“에러 return은 먼저, 정상 return은 마지막에”