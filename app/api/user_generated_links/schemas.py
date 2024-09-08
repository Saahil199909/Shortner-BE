from pydantic import BaseModel, validator
from fastapi import HTTPException, status


class ShortlinkUpdateSchema(BaseModel):
    long_url: str

    @validator('long_url', pre=True)
    def handle_empty_string(cls, value):
        if value == "":
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail='Value cannot be empty string')
        return value