#study_room_router.py

#채팅방 관련 API 전용 입구 (생성,조회 삭제 여기서 처리됨)

from fastapi import APIRouter, Depends #Depends = fastapi 의존성 주입 기능 ,필요한 기능 자동 실행
from sqlalchemy.orm import Session
from pydantic import BaseModel
from db.database import get_db
from core.dependencies import get_current_user #(JWT 사용자 인증 역할 파일의 함수 가져오기)
from services.room_service import (create_study_room, get_user_rooms, delete_room)
# from services.room_service import get_user_rooms
from services.chat_message_service import get_chat_messages
# from services.room_service import delete_room



#==============

router = APIRouter()


# 1.요청 데이터 구조 생성(채팅방 생성 요청 데이터 구조 정의)
# 사용자가 보낼 JSON 구조를 정하기 위해 필요.
class CreateRoomRequest(BaseModel):
    title: str
    
# 2.채팅방 생성 API 함수,라우터 시작 
@router.post("/rooms")

def create_room(
    request: CreateRoomRequest, #사용자 JSON 데이터 받기
    db: Session = Depends(get_db), #DB연결 자동 주입
    current_user = Depends(get_current_user) #현재 로그인 사용자 자동 조회
):
    
    #service  함수 시작
    room = create_study_room(
        db=db,#DB연결 전달
        user_id=current_user.id, #현재 로그인 사용자 ID전달
        title=request.title #사용자가 입력한 제목 전달
    )
    return room

# 3.room목록 조회 api함수 시작
#GET 방식 /rooms api 생성 (데이터 조회 =get)
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
#채팅방별 메시지 불러오는 라우터 추가 (/rooms/1/messages 요청 들어오면 실행)
@router.get("/rooms/{room_id}/messages")

def get_room_message(
    room_id: int, #각 채팅방별 번호
    db: Session = Depends(get_db), #db연결
    current_user = Depends(get_current_user)#현재 로그인 사용자 확인
):
    messages = get_chat_messages(db, room_id) #메시지 조회   
    
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