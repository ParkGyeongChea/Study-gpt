#user_schema.py

#API 요청/응답 데이터 검증
#회원가입이 요청이 들어오면, 이메일,비밀번호, 타입이 맞는지 검사하는 역할

from pydantic import BaseModel
#BaseModel = API 데이터 검증용 부모 클래스



# 1.실제 회원가입 요청 데이터 구조 생성 ,회원가입 요청 데이터 형식 정의
class UserCreate(BaseModel):
    email:str
    password:str
#FastAPI 가 이런 JSON만 허용
# {
#   "email": "test@gmail.com",
#   "password": "1234"
# }


# 2.로그인 요청 데이터 구조 생성
class UserLogin(BaseModel):
    
    email: str
    password: str
    
#UserCreate 와 별개로 따로 만드는 이유

# 지금은 UserCreate 와 같아 보이지만, 나중에는

# 기능	필요한 데이터
# 회원가입	email + password + nickname
# 로그인	email + password

# 이렇게 달라질 수 있다.