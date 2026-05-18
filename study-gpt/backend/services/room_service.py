#room_service.py

#실제로 채팅방을 DB에 저장하는 역할의 파일
#채팅방 생성/ 채팅방 목록 조회 로직을 처리하는 서비스 파일

from models.study_room import StudyRoom
from services.llm_service import llm
from sqlalchemy import desc
#desc = 정렬을 내림차순으로 하겠다는 뜻 , 최신 날짜 -> 오래된날짜 순서로 정렬할떄 사용


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

# 2.현재 사용자의 room 목록(채팅방 목록) 조회,가져옴
def get_user_rooms(db, user_id):
    
    
    #studyroom 테이블 조회 시작
    rooms = (
        db.query(StudyRoom).filter(StudyRoom.user_id == user_id).order_by(desc(StudyRoom.updated_at)).all()
        #studyroom 테이블 조회 시작/ 현재 로그인한 사용자의 채팅방만 조회/ updated_at이 가장 최신인 채팅방부터 정렬
        #조회 결과를 리스트로 전부 가져옴
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

# 4. 채팅방 제목을 실제 DB에 저장하는 제목 수정 함수
def update_room_title(db, room_id, new_title):
    
    #room_id 기준으로 room 조회
    room = db.query(StudyRoom).filter(StudyRoom.id == room_id).first()
    
    #room 없으면 종료
    if not room:
        return None
    #room 제목 수정
    room.title = new_title
    
    # 실제 DB 저장
    db.commit()

    # 수정된 최신 DB 상태 다시 반영
    db.refresh(room)

    # 수정 완료된 room 반환
    return room