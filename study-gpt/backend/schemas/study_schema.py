from pydantic import BaseModel

class StudyRequest(BaseModel):
    message: str