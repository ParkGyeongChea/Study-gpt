#graph_state.py

#랭그래프 핵심 구조 시작
# AI Agent 의 기억 공간 파일

#State = 현재 AI 가 알고 있는 모든 정보
#현재 프로젝트에는 학습 흐름에 필요한 정보들이 있음(사용자 입력, intent, category, topic, study_mode, 현재 step, AI 응답)
#지금까지는 이 값들이, 함수 인자 ( run(message, study_mode) ) 로 따로 따로 움직였다.

#랭그래프에서는 이걸 전부 하나의 state객체 안에서 관리한다.
#즉 앞으로 흐름은 State -> Node 실행 -> State 수정 -> 다음 Node 이동 형태가 됨

#Node = 하나의 작업을 수행하는 단계(함수) , 사용자 의도 분석, 커리큘럼 생성, 다음 step 계산, 퀴즈 생성, 답변 생성

#여기서는 State 구조 정의를 해야함.

# TypedDict = 딕셔너리 설계도.

# {
#     "message": "...",
#     "intent": "study"
# }
# 이러한 키들이 있을떄, 이 딕셔너리는 어떤 키들을 가져야 하는지 정의한다.
# 랭그래프는 State 기반 시스템이기 떄문에, 어떤 데이터가 흐르는지 명확하게 정의해야 한다.

#=================================================

from typing import TypedDict #딕셔너리 구조 타입 정의

# 1. 랭그래프 전체 상태 설계도, AI가 현재 기억해야 하는 데이터 목록

# GraphState 는 왜 존재? 랭그래프에서는 Node 들이 서로 직접 데이터를 주고받지 않는다.
# 전부 State 객체 하나를 공유한다.

class GraphState(TypedDict): #GraphState 는 반드시 이런 값들을 가진다고 정의
    message: str
    intent: str
    category: str
    topic: str
    level: str
    response: str
    
    #즉 앞으로 Node들은 state["message"] 이런 식으로 값을 읽고 수정하게 됨.
    
    #intent Node 
    #흐름 시작점은 , 사용자 입력 -> 의도 분석으로 시작 그래서 맨 처음 작성
    
    