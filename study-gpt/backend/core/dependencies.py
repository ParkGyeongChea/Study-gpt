#dependencies.py

#현재 로그인 사용자 조회 전용 파일

from sqlalchemy.orm import Session 
from fastapi import HTTPException, Depends
from db.database import get_db 
from services.user_service import get_user_by_id 
from core.security import get_user_id_from_token
from fastapi.security import OAuth2PasswordBearer



# ======================================================================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


# 1.JWT 토큰을 이용해서 현재 로그인한 사용자(User 객체) 를 가져오는 함수 생성.

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
     
    user_id = get_user_id_from_token(token)
    #JWT 해석해서 user_id 꺼내기
    
    if not user_id:
        raise HTTPException(status_code=401)
    #토큰 해석 ,JWT 인증 실패 처리

    user = get_user_by_id(db, user_id)
    #id 기준으로 DB에서 실제 사용자 조회
    
    return user