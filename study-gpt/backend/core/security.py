#security.py

#프로젝트 공통 보안 기능
#bcrypt 담당+ jwt 보안 담당 파일 (비밀번호 암호화 + JWT 생성 + JWT 검증 담당 파일)


from passlib.context import CryptContext #CryptContext = 비밀번호 암호화 관리자
from jose import jwt, JWTError 
#jwt 생성/해석 라이브러리 불러오기 JWTError= JWT 오류 처리용
#JWT는 토큰 위조, 만료 , 형식 이상, 시크릿 키 불일치 , 실패 가능성이 있다
#이 코드가 없으면 오류 시 예외처리가 불가능하고 서버 500 에러가 날수 있음

from datetime import datetime, timedelta #datetime 라이브러리에서 현재 시간 생성, 시간 계산 기능 불러오기


#=========================================================================

SECRET_KEY = "study-gpt-secret-key" #나중에 env로 뺄 예정
ALGORITHM = "HS256" #jwt 암호화 방식
ACCESS_TOKEN_EXPIRE_MINUTES = 60 #토큰 만료 시간, 60분

pwd_context = CryptContext(
    #bcrypt 암호화 설정 생성
    #pwd_context 는 비밀번호 암호화 도구 같은 객체.
    #이 객체로 비밀번호 암호화, 비밀번호 비교 검증 수행
    
    schemes=["bcrypt"], ##bcrypt 암호화 설정 생성
    deprecated="auto" #bcrypt 최신 방식 유지용 설정
)

# 1.실제 비밀번호 암호화 함수 생성
def hash_password(password: str):

    return pwd_context.hash(password) #핵심. bcrypt 암호화 수행

# 2.입력 비밀번호와 DB암호화 비밀번호 비교 함수 추가
def verify_password(
    plain_password: str, #사용자가 방금 입력한 원본 비밀번호
    hashed_password: str #DB에 저장된 bcrypt 해시 문자열
):

    return pwd_context.verify(
        #pwd_context.verify(...) = bcrypt 비교 수행 . 비밀번호 같으면 true, 다르면 false
        plain_password,
        hashed_password
    )

# 3. JWT 토큰 생성 핵심 함수 생성
def create_access_token(user_id: int):
    
    expire = datetime.utcnow() + timedelta(
    minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    #datetime.utcnow() = 현재 시간 가져오기 timedelta(minutes=60) = 60분 추가 -> 토큰 만료 시간을 현재시간+60분
    )
    
    #JWT 안에 들어갈 데이터 생성
    payload ={
        "sub":str(user_id), #사용자 번호 저장
        "exp":expire #exp= 시간 만료 저장
    }
    
    #JWT 생성
    token = jwt.encode(
        payload, #토큰 안에 저장할 데이터
        SECRET_KEY, #암호화 비밀키
        algorithm=ALGORITHM #암호화 방식
    )
    
    return token

# 4.JWT 안에서 user_id를 추출하는 함수 생성
def get_user_id_from_token(token: str):
    
   
    
    try:
        
        print("받은 JWT:", token)
        
        #payload = 데이터
        payload = jwt.decode( #jwt 해석 함수
            token, #사용자가 보낸 jwt
            SECRET_KEY, #jwt 생성 때 사용한 비밀키
            algorithms=[ALGORITHM] #jwt 암호화 방식 지정 (HS256 사용중)
        )
        print("decode 성공 payload:", payload)
        
        user_id = payload.get("sub") 
        #payload(데이터) 안에 저장된 sub 값 꺼내기
        #sub는 jwt에서 로그인 사용자 정보 저장용 표준 키.
        
        return int(user_id)
        #왜 int 변환? 
        #jwt 저장 시, str(user_id) 로 문자열 저장했기 때문에, 숫자로 다시 복원하는것
        
        #이대로 쓰면 위조,만료,이상한 토큰이 들어오면 서버가 터질 수 있으니, try~except 구문으로 서버 종료 방지.
        
    except JWTError as e:
        
        print("JWT 에러 발생:", e)
        
        return None
    
    
