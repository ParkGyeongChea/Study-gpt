# user_service.py
# 사용자 회원가입 / 로그인 / 회원탈퇴 관련 서비스 함수 모음

from sqlalchemy.orm import Session

from models.user import User

from core.security import (
    hash_password,
    verify_password
)

# ==========================================
# 회원가입 함수
# ==========================================

def create_user(
    db: Session,
    email: str,
    password: str
):

    # 같은 이메일 사용자 존재 여부 확인
    existing_user = db.query(User).filter(
        User.email == email
    ).first()

    # 이미 존재하는 이메일이면 회원가입 실패
    if existing_user:
        return None


    # 비밀번호 암호화
    hashed_password = hash_password(password)


    # User 객체 생성
    user = User(
        email=email,
        password=hashed_password
    )

    # DB 저장 예약
    db.add(user)

    # 실제 DB 반영
    db.commit()

    # 저장된 최신 데이터 다시 조회
    db.refresh(user)

    return user


# ==========================================
# 로그인 인증 함수
# ==========================================

def authenticate_user(
    db: Session,
    email: str,
    password: str
):

    # 이메일 기준 사용자 조회
    user = db.query(User).filter(
        User.email == email
    ).first()


    # 사용자 없으면 로그인 실패
    if not user:
        return None


    # 비밀번호 검증 실패 시 로그인 실패
    if not verify_password(
        password,
        user.password
    ):
        return None


    # 로그인 성공
    return user


# ==========================================
# id 기준 사용자 조회 함수
# ==========================================

def get_user_by_id(
    db: Session,
    user_id: int
):

    return db.query(User).filter(
        User.id == user_id
    ).first()


# ==========================================
# 회원탈퇴 함수
# ==========================================

def delete_user(
    db: Session,
    user_id: int
):

    # 삭제할 사용자 조회
    user = db.query(User).filter(
        User.id == user_id
    ).first()


    # 사용자가 없으면 실패
    if not user:
        return False


    # 사용자 삭제
    db.delete(user)

    # 실제 DB 반영
    db.commit()

    return True