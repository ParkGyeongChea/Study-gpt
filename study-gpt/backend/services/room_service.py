#room_service.py

#실제로 채팅방을 DB에 저장하는 역할의 파일
#채팅방 생성/ 채팅방 목록 조회 로직을 처리하는 서비스 파일

from models.study_room import StudyRoom
from models.study_session import StudySession
from models.chat_message import ChatMessage
from services.shared_llm import llm
from sqlalchemy import desc



#===================================

# 1.새 채팅방 생성 함수
def create_study_room(db, user_id, title):

    #새로운 studyroom 객체 생성
    new_room = StudyRoom(
        user_id=user_id,
        title=title, 
    )
    
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    
    return new_room

# 2.현재 사용자의 room 목록(채팅방 목록) 조회,가져옴
def get_user_rooms(db, user_id):
    
    
    #studyroom 테이블 조회 시작
    rooms = (
        db.query(StudyRoom).filter(StudyRoom.user_id == user_id).order_by(desc(StudyRoom.updated_at)).all()
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



# 4. 채팅방 삭제 함수
def delete_room(db, room_id):
    
    
    room = db.query(StudyRoom).filter(
        StudyRoom.id == room_id
    ).first()

    if not room:
        return None
    
    # 현재 room의 자식 room들 조회
    child_rooms = db.query(StudyRoom).filter(
        StudyRoom.parent_room_id == room_id
    ).all()

    # 자식 room들을 최상위 room으로 승격
    for child in child_rooms:

        child.parent_room_id = None
        
    # 현재 room에 연결된 채팅 메시지 삭제
    db.query(ChatMessage).filter(
        ChatMessage.room_id == room_id
    ).delete()

    # 현재 room에 연결된 학습 세션 삭제
    db.query(StudySession).filter(
        StudySession.room_id == room_id
    ).delete()
    

    db.delete(room)
    db.commit()

    return True

# 5.채팅방 이름 변경 함수 
def update_room_title(db, room_id: int, user_id: int, title: str):
    
    # room 조회,id 기준으로 채팅방 찾기
    room = db.query(StudyRoom).filter(
        StudyRoom.id == room_id,
        StudyRoom.user_id == user_id
    ).first()
    
    if not room:
        return None
    
    room.title = title
    
    db.commit()
    db.refresh(room)
    return room


# 6. 채팅방을 학습 아카이브 <-> 현재 학습으로 이동하는 함수
def move_room_to_archive(db, room_id: int, user_id: int):
    
    #현재 사용자의 room 조회
    room = db.query(StudyRoom).filter(
        StudyRoom.id == room_id,
        StudyRoom.user_id == user_id
    ).first()
    
    if not room:
        return None
    
    # 현재 변경될 archive 상태 저장
    new_archive_state = not room.is_archived
    
    ## 현재 상태 반대로 변경
    room.is_archived = new_archive_state
    
    if new_archive_state:
        room.parent_room_id = None

    # 하위 자식 room 전체 archive 상태 변경
    # 함수 안의 함수, 특정 함수 안에서만 사용하는 보조 기능
    def update_children_archive(parent_id):

        children = db.query(StudyRoom).filter(
            StudyRoom.parent_room_id == parent_id
        ).all()

        for child in children:
            child.is_archived = new_archive_state

            update_children_archive(child.id)


    update_children_archive(room.id)
    
    db.commit()
    db.refresh(room)
    
    return room

#7. 부모 room 변경 함수
def update_parent_room(db, room_id: int, user_id: int, parent_room_id: int | None):
    
    # 현재 room 조회
    room = db.query(StudyRoom).filter(
        StudyRoom.id == room_id,
        StudyRoom.user_id == user_id
    ).first()

    # room 없으면 종료
    if not room:
        return None

    # 부모 room 변경
    room.parent_room_id = parent_room_id

    db.commit()
    db.refresh(room)
    return room

