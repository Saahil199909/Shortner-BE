from pydantic import BaseModel, field_validator

from fastapi import APIRouter, Depends,  HTTPException, status

class GeneratorSchema(BaseModel):
    user_id: int 
    key_length: str
    long_url: str
    domain: str

    @field_validator('long_url', 'key_length', mode="before")
    def handle_empty_string(cls, value, info):
        if value == "" or value is None:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail=f"{info.field_name}: Value should not be empty")
        return value
