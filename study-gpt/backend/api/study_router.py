#study_router.py

#사용자가 보낸 요청을 처음 받는 파일. service 호출만 함.

from fastapi import APIRouter 
from services.curriculum_service import start_study_service 
from pydantic import BaseModel 
from typing import List

router = APIRouter() 

class StudyRequest(BaseModel): 
    message: str               

class StudyResponse(BaseModel):
    
    category: str 
    curriculum: List[str] 
                            
                            
@router.post("/study/start", response_model=StudyResponse) 

       
def start_study(request: StudyRequest):

    message = request.message
    result = start_study_service(message) 
    return result 
    