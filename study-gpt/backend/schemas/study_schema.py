#study_schema.py

from typing import Optional
from pydantic import BaseModel

class StudyRequest(BaseModel):
    
    #현재 어느 채팅방에서 대화 중인지 저장
    room_id: int
    
    message: str
    
    study_mode: Optional[str] = None #사용자가 선택한 학습 모드를 받을 수 있게 하는 코드.
    #Optional = 문자열이 들어올 수도 있고, 안 들어올 수도 있다는 뜻
    #Optional[str] = None 때문에, study_mode가 없어도 요청 가능
    