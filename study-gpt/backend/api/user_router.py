#user_router.py

#회원가입 API

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.user_schema import UserCreate, UserLogin
from services.user_service import (create_user, authenticate_user, delete_user)
from core.security import create_access_token
from core.dependencies import get_current_user
from fastapi import HTTPException 

#=============================================

#라우터 생성
#실제 회원가입 API 그룹 생성
router = APIRouter()


#1. 회원가입 API endpoint 생성
#POST /signup API 생성 , "/signup" 주소로 오는 POST 요청 처리
@router.post("/signup")

#실제 회원가입 API 함수
def signup( 
    user_data: UserCreate,
    db: Session = Depends(get_db) 
):
    new_user = create_user(db,user_data.email, user_data.password)
    
    #회원가입 성공 결과 사용자에게 반환
    return {
        "message":"회원가입이 완료되었습니다.",
        "email": new_user.email
    }
    
#2.로그인 POST API 생성

@router.post("/login")

#로그인 API함수
def login(
    data: UserLogin,
    db: Session = Depends(get_db)    
):
    #로그인 가능한 유저인지 검사
    user = authenticate_user(  
        db,
        data.email, 
        data.password 
    )
    
    #로그인 실패 시 에러 메시지를 json으로 반환 = return {}
    if not user:
        raise HTTPException(
            status_code=401,
            detail="이메일 또는 비밀번호가 올바르지 않습니다."
        )
          
    # 로그인 성공 시, 로그인한 사용자의 id를 이용해서 JWT access_token 생성
    access_token = create_access_token(user.id)

    # 생성된 JWT 토큰을 사용자에게 반환
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "email": user.email
    }


# 3. 현재 로그인 사용자 정보 반환 api 함수 생성
#테스트용 보호 API 생성 , /me = JWT 인증 테스트 API

@router.get("/me")
def get_me(current_user = Depends(get_current_user)):
    
    return {"email": current_user.email}


# 4. 회원탈퇴 API 추가 , DELETE 요청용 회원탈퇴 API 생성
@router.delete("/users/me")
def delete_me(

    # DB 연결
    db: Session = Depends(get_db),

    # 현재 JWT 로그인 사용자 정보
    current_user = Depends(get_current_user)
):
    # 회원 삭제 실행
    delete_user(db,current_user.id) 

    return {"message": "회원탈퇴가 완료되었습니다."}