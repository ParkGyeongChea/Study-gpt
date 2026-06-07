#study_schema.py

from typing import Optional
from pydantic import BaseModel

class StudyRequest(BaseModel):
    
    room_id: Optional[int] = None

    message: str
    
    study_mode: Optional[str] = None 
    
    