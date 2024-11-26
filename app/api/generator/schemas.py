from pydantic import BaseModel, validator

from fastapi import APIRouter, Depends,  HTTPException, status

class GeneratorSchema(BaseModel):
    user_id: int 
    key_length: str
    long_url: str
    domain: str

    @validator('long_url', 'key_length', pre=True)
    def handle_empty_string(cls, value):
        if value == "":
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail='Long Url should not be empty')
        return value
