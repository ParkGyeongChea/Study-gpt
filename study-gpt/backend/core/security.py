#security.py

#프로젝트 공통 보안 기능

from passlib.context import CryptContext #CryptContext = 비밀번호 암호화 관리자

pwd_context = CryptContext(
    #bcrypt 암호화 설정 생성
    #pwd_context 는 비밀번호 암호화 도구 같은 객체.
    #이 객체로 비밀번호 암호화, 비밀번호 비교 검증 수행
    
    schemes=["bcrypt"], ##bcrypt 암호화 설정 생성
    deprecated="auto" #bcrypt 최신 방식 유지용 설정
)

#실제 비밀번호 암호화 함수 생성
def hash_password(password: str):

    return pwd_context.hash(password) #핵심. bcrypt 암호화 수행

#입력 비밀번호와 DB암호화 비밀번호 비교 함수 추가
def verify_password(
    plain_password: str, #사용자가 방금 입력한 원본 비밀번호
    hashed_password: str #DB에 저장된 bcrypt 해시 문자열
):

    return pwd_context.verify(
        #pwd_context.verify(...) = bcrypt 비교 수행 . 비밀번호 같으면 true, 다르면 false
        plain_password,
        hashed_password
    )