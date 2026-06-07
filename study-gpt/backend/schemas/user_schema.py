#user_schema.py

#API 요청/응답 데이터 검증
#회원가입이 요청이 들어오면, 이메일,비밀번호, 타입이 맞는지 검사하는 역할

from pydantic import BaseModel


#=======================================

# 1.실제 회원가입 요청 데이터 구조 생성 ,회원가입 요청 데이터 형식 정의
class UserCreate(BaseModel):
    email:str
    password:str

# 2.로그인 요청 데이터 구조 생성
class UserLogin(BaseModel):
    
    email: str
    password: str
    
