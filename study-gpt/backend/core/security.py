#security.py

#프로젝트 공통 보안 기능
#bcrypt 담당+ jwt 보안 담당 파일 (비밀번호 암호화 + JWT 생성 + JWT 검증 담당 파일)


from passlib.context import CryptContext 
from jose import jwt, JWTError 
from datetime import datetime, timedelta 


#=========================================================================

SECRET_KEY = "study-gpt-secret-key" 
ALGORITHM = "HS256" 
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30 #토큰(로그인 시간) 만료 시간 30일

#bcrypt 암호화 설정 생성
pwd_context = CryptContext(
    schemes=["bcrypt"], 
    deprecated="auto" 
)

# 1.실제 비밀번호 암호화 함수 생성
def hash_password(password: str):

    return pwd_context.hash(password) 

# 2.입력 비밀번호와 DB암호화 비밀번호 비교 함수 추가
def verify_password(
    plain_password: str, 
    hashed_password: str 
):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )

# 3. JWT 토큰 생성 핵심 함수 생성
def create_access_token(user_id: int):
    
    expire = datetime.utcnow() + timedelta(
    minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    
    #JWT 안에 들어갈 데이터 생성
    payload ={
        "sub":str(user_id),
        "exp":expire 
    }
    
    #JWT 생성
    token = jwt.encode(
        payload, 
        SECRET_KEY, 
        algorithm=ALGORITHM 
    )
    
    return token

# 4.JWT 안에서 user_id를 추출하는 함수 생성
def get_user_id_from_token(token: str):
    
    try:
        print("받은 JWT:", token)

        
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        print("decode 성공 payload:", payload)
        
        user_id = payload.get("sub") 
        
        
        return int(user_id)
        
        
    except JWTError as e:
        
        print("JWT 에러 발생:", e)
        
        return None
    
    
