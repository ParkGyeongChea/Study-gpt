#user_router.py

#회원가입 API

#라우터를 만드는 이유 = FastAPI 에서는 보통 라우터(Api)입구를 따로 관리함

from fastapi import APIRouter, Depends
#APIRouter = API 그룹 생성 도구
#Depends = FastAPI 핵심 기능 중 하나. 필요한 기능 자동 주입 (나중에 db: Session = Depends(get_db) 형태로 사용)

from sqlalchemy.orm import Session
#sqlalchemy.orm = orm 기능을 모아둔 공간
#orm = class User(Base) 같은 파이썬 코드로, db테이블을 조작하게 해주는 시스템
#보통 DB는 SQL을 써야 하지만, ORM 을 사용하면 파이썬 객체로 DB작업이 가능.


#회원가입,로그인 API에 필요한 기능(회원가입 검증 함수, 로그인 검증 함수)들 가져오기
from db.database import get_db
from schemas.user_schema import UserCreate, UserLogin
from services.user_service import create_user,authenticate_user



#===============

#라우터 생성
#실제 회원가입 API 그룹 생성
router = APIRouter()


#1. 회원가입 API endpoint 생성
#POST /signup API 생성 , "/signup" 주소로 오는 POST 요청 처리
@router.post("/signup")

#실제 회원가입 API 함수
def signup( #회원가입 요청을 받아서 DB저장 함수 실행 준비
    user_data: UserCreate, #회워나입 요청 데이터
    db: Session = Depends(get_db) #DB연결(Session) 자동 실행 , Depends(get_db)="DB연결 자동으로 준비"
):
    new_user = create_user(db,user_data) #회원가입 데이터를 db에 저장 create_user = 회원가입 저장 서비스 함수
    
    #회원가입 성공 결과 사용자에게 반환
    return {
        "message":"회원가입이 완료되었습니다.",
        "email": new_user.email
    }
    
#2.로그인 POST API 생성

@router.post("/login")

#로그인 API함수
def login(
    user_data: UserLogin, #로그인 요청 데이터
    db: Session = Depends(get_db) 
    #get_db() 실행해서, db연결(session) 자동으로 넣음.
    # Depends = 자동으로 준비해라 , 필요한 기능 자동 주입.
):
    #로그인 가능한 유저인지 검사
    user = authenticate_user(  #authenticate_user = 이메일로 유저 조회, 존재 확인, bcrypt 비밀번호 비교, 성공시 유저 반환 역할
        db, #현재 연결 db전달
        user_data.email, #로그인 요청 email 값
        user_data.password # 요청 비밀번호 값
        
        #user = 로그인 성공한 유저 결과 저장. 로그인 성공 시, 안에 user 객체 들어감 실패 시 None
    )
    
    #로그인 실패 시 에러 메시지를 json으로 반환 = return {}
    if not user:
        return {"message": "이메일 또는 비밀번호가 올바르지 않습니다."} 
          
    #로그인 성공 시 메시지 반환
    return {
        "message": "로그인 성공",
        "email": user.email
    }