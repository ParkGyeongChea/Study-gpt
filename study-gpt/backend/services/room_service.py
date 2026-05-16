#room_service.py

#실제로 채팅방을 DB에 저장하는 역할의 파일

from models.study_room import StudyRoom
from services.llm_service import llm



#===================================

# 1.새 채팅방 생성 함수
def create_study_room(db, user_id, title):
# def create_study_room(db, user_id, message): 추후에 프론트 연결 후 수정
    
    #사용자 첫 메시지 기반 room 제목 생성
    # title = generate_room_title(message) #추후에 프론트 연결 후 수정
    
    #새로운 studyroom 객체 생성
    new_room = StudyRoom(
        user_id=user_id,#유저 아이디
        title=title, #채팅방 제목
    )
    
    #DB에 저장 및 새로고침
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    
    return new_room

# 2.현재 사용자의 room 목록 조회
def get_user_rooms(db, user_id):
    
    
    #studyroom 테이블 조회 시작
    rooms = (
        db.query(StudyRoom)
        .filter(StudyRoom.user_id == user_id) # 현재 사용자 room만 필터링,
        .all() #조회 결과 전부 가져오기
    )

    return rooms

# 3.채팅방 제목 자동 생성 함수
# 추후 자동 채팅방 제목 생성 기능 연결 예정
def generate_room_title(message: str):
    
    prompt = f"""
    사용자의 학습 요청 메시지를 보고
    짧고 자연스러운 채팅방 제목을 생성하라.

    사용자 입력:
    "{message}"

    규칙:
    - 제목만 출력
    - 10자 내외
    - 불필요한 설명 금지
    """
    
    response = llm.invoke(prompt)
    title = response.content.strip()
    
    return title