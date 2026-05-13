#user_service.py
#회원가입 -> DB저장

from sqlalchemy.orm import Session 
#Session = DB작업 공간 타입

from models.user import User
from schemas.user_schema import UserCreate
from fastapi import HTTPException
from core.security import hash_password
from core.security import verify_password


# 1. DB 저장 함수 추가
#회원가입 데이터를 받아서, users 테이블에 저장하는 함수
def create_user(db: Session, user_data: UserCreate):
    
    # 같은 이메일 유저 있는지 검색
    existing_user = get_user_by_email(db, user_data.email)

    # 이미 존재하면 회원가입 실패
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="이미 존재하는 이메일입니다."
        )
    
    new_user = User( #회원가입 데이터를 이용해서 User테이블 객체 생성
        email=user_data.email,
        password=hash_password(user_data.password)
        #이 코드로 인해, 사용자가 비밀번호를 입력하면 -> bcrypt 암호화-> 암호화 문자열 저장
    )
    
    db.add(new_user) #new_user 객체를 DB 저장 대상에 등록 , 이 데이터를 저장할 예정이다 라고 DB Session 에 등록만 함
    
    db.commit() #db에 실제 저장 확정
    
    db.refresh(new_user) #db에 저장된 최신 상태 다시 가져오기 , 저장 후 다시 불러와서 저장결과 다시 확인
    
    return new_user


# 2.email 기준으로 유저 조회 함수 추가
def get_user_by_email(
    db: Session,
    email: str
    #사용자 로그인 후 DB에서 유저 검색
):

    return db.query(User).filter(
        #db.query = users 테이블 조회 시작
        
        User.email == email
        #.filter(User.email == email)  = email 같은 유저 찾기
        
    ).first() #첫 번째 결과 하나만 가져오기, 보통 유저 1명만 존재하기 때문에 first()
    
# 3. 로그인 가능한 사용자 검증 함수 추가
def authenticate_user( 
    db: Session, #DB연결
    email: str, #로그인 email 입력
    password: str #로그인 password 입력
):
    user = get_user_by_email(db, email) 
    #로그인 요청으로 들어온 email을 기준으로, users 테이블에서 해당 유저를 찾는다.
    
    #존재하지 않는 이메일 처리
    if not user:
        return None
    
    #입력 비밀번호와 DB암호화 비밀번호 비교 함수(security.py의 함수)를 이용해서 비밀번호가 다르면 로그인 실패
    if not verify_password(password, user.password):
        return None
    
    return user

    #여기까지 흐름 -> user = get_user_by_email(db, email) 로 유저 찾음
    #존재하지 않는 이메일(유저가 없는경우)  if not user:
    # bcrypt 비밀번호 비교, 비밀번호가 진짜 맞는지 검사 ->if not verify_password(...):
    
    #authenticate_user() 역할은
    #이 유저가 진짜 로그인 가능한지 판단하는 함수.
    