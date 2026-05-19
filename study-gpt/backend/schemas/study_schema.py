#study_schema.py

from typing import Optional
from pydantic import BaseModel

class StudyRequest(BaseModel):
    
    #현재 어느 채팅방에서 대화 중인지 저장, int 또는 None 허용
    #즉 room_id 숫자가 들어와도 되고 안 들어와도 된다 
    room_id: Optional[int] = None
    #Optional[int] int 또는 None 허용, 기본값은 None
    #프론트가 room_id를 안 보내도 에러 내지 마라 
    
    message: str
    
    study_mode: Optional[str] = None #사용자가 선택한 학습 모드를 받을 수 있게 하는 코드.
    #Optional = 문자열이 들어올 수도 있고, 안 들어올 수도 있다는 뜻
    #Optional[str] = None 때문에, study_mode가 없어도 요청 가능
    