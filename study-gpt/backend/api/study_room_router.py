#study_room_router.py

#채팅방 관련 API 전용 입구 (생성,조회 삭제 여기서 처리됨)

from fastapi import APIRouter, Depends 
from sqlalchemy.orm import Session
from pydantic import BaseModel
from db.database import get_db
from core.dependencies import get_current_user 
from services.room_service import (
    create_study_room,
    get_user_rooms,
    delete_room,
    update_room_title,
    move_room_to_archive,
    update_parent_room
)
from services.chat_message_service import get_chat_messages
from models.study_room import StudyRoom

#=======================================

router = APIRouter()


# 1.요청 데이터 구조 생성(채팅방 생성 요청 데이터 구조 정의)

class CreateRoomRequest(BaseModel):
    title: str

class UpdateRoomTitleRequest(BaseModel):
    title: str
    
# 부모 room 변경 요청 데이터
class UpdateParentRoomRequest(BaseModel):
    parent_room_id: int | None 
    
# 2.채팅방 생성 API 함수,라우터 시작 

@router.post("/rooms")

def create_room(
    request: CreateRoomRequest,
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    
    #service  함수 시작
    room = create_study_room(
        db=db,
        user_id=current_user.id,
        title=request.title
    )
    return room

# 3.room목록 조회 api함수 시작
@router.get("/rooms")

def get_rooms(
    db: Session = Depends(get_db), #db연결 자동 주입
    current_user = Depends(get_current_user)
):
    rooms = get_user_rooms(
        db=db,
        user_id=current_user.id 
    )
    
    return rooms
# 4.각 채팅방(room)별 메시지 불러오기
@router.get("/rooms/{room_id}/messages")

def get_room_message(
    room_id: int,
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    messages = get_chat_messages(db, room_id) 
    return messages


# 5. 채팅방 삭제 API ,함수 추가
@router.delete("/rooms/{room_id}")

def remove_room(
    room_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # room 삭제 실행
    delete_room(db, room_id)

    return {
        "message": "채팅방 삭제 완료"
    }
    
# 6. 채팅방 이름 변경 API
@router.put("/rooms/{room_id}")
def update_room(
    room_id: int,
    request: UpdateRoomTitleRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    updated_room = update_room_title(
        db,
        room_id,
        current_user.id,
        request.title
    )

    if not updated_room:
        return {
            "error": "Room not found"
        }

    return {
        "id": updated_room.id,
        "title": updated_room.title
    }
    
# 7.채팅방 이동 라우터 및 함수 추가
@router.put("/rooms/{room_id}/archive")

def archive_room(
    room_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    archived_room = move_room_to_archive(
        db,
        room_id,
        current_user.id
    )

    # room 없으면 에러 반환
    if not archived_room:
        return {
            "error": "Room not found"
        }

    return {
        "message": "채팅방 이동 완료",
        "room_id": archived_room.id,
        "is_archived": archived_room.is_archived
    }

# 8. 부모 room 변경 API
@router.put("/rooms/{room_id}/parent")

def update_room_parent(
    room_id: int,
    request: UpdateParentRoomRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    # 현재 사용자의 room 조회
    room = db.query(StudyRoom).filter(
        StudyRoom.id == room_id,
        StudyRoom.user_id == current_user.id
    ).first()

    # room 없으면 종료
    if not room:
        return {
            "error": "Room not found"
        }

    # 부모 room 변경
    room.parent_room_id = request.parent_room_id

    db.commit()
    db.refresh(room)

    return {
        "message": "부모 room 변경 완료",
        "room_id": room.id,
        "parent_room_id": room.parent_room_id
    }