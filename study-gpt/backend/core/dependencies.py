#dependencies.py

#현재 로그인 사용자 조회 전용 파일

from sqlalchemy.orm import Session #DB ORM 기능을 모은 것 에서 , DB작업 공간 역할을 하는 Session 타입 불러옴

from fastapi import HTTPException, Depends

#fastapi 라이브러리(API 서버 기능 담당 공간)의
# 에러 응답 생성 역할의 HTTPException,
# 필요한 기능(DB 연결 등)을 자동 주입하는 역할의 Depends 기능 불러오기

from db.database import get_db #db/database(DB 연결 생성 및 반환 담당 파일)의 DB 연결(Session) 을 생성하는 역할을 하는 get_db 함수 불러옴

from services.user_service import get_user_by_id #id 기준으로 조회하는 역할을 하는 함수 불러오기

from core.security import get_user_id_from_token
# core/security.py 파일 (JWT 생성/검증 담당 파일)의 JWT 안에서 user_id를 추출하는 역할의 get_user_id_from_token 함수 불러오기

from fastapi.security import OAuth2PasswordBearer
# fastapi.security 공간 (FastAPI 공식 인증 시스템 모음)의 JWT Bearer 인증 처리 역할을 하는 OAuth2PasswordBearer 기능 불러오기


# ======================================================================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

#oauth2_scheme = JWT 인증 처리 객체 저장 변수
#OAuth2PasswordBearer = FastAPI 공식 JWT Bearer 인증 시스템 생성
#tokenUrl="/login" = JWT를 발급하는 로그인  API 주소




# 1.JWT 토큰을 이용해서 현재 로그인한 사용자(User 객체) 를 가져오는 함수.
#   중요한 함수. 앞으로의 모든 기능이 이걸 사용함(비밀번호 변경, 사용자별 진행도 저장, 사이드챗, 보호 API , 내 정보 조회)
#   전부 Depends(get_current_user) 형태로 연결됨
#   사용자 로그인시 검사원 역할

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    # authorization 변수 = 사용자가 요청 헤더에 보낸 JWT 토큰 값을 저장하는 변수

    # Header(None) = FastAPI가 요청 헤더의 Authorization 값을 자동으로 꺼내서 넣어줌
    # 예: Authorization: Bearer eyJhbGc...

    # JWT는 요청 헤더로 전달되기 때문에이 코드가 없으면 서버가 JWT 토큰을 받을 수 없음

    # db: Session = DB 연결 객체를 저장할 변수

    # Depends(get_db) = get_db() 함수를 자동 실행해서 DB 연결(Session)을 준비해주는 FastAPI 기능

    # JWT 검증 후, user_id를 이용해서 실제 사용자를 DB에서 조회하기 위해 필요
    

    
    user_id = get_user_id_from_token(token)
    #JWT 해석해서 user_id 꺼내기
    
    if not user_id:
        raise HTTPException(status_code=401)
    #토큰 해석 ,JWT 인증 실패 처리

    user = get_user_by_id(db, user_id)
    #id 기준으로 DB에서 실제 사용자 조회
    
    return user