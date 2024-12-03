from pydantic import BaseModel, validator, EmailStr
from fastapi import HTTPException


class UserSchema(BaseModel):
    email: EmailStr
    password: str

    @validator('password', pre=True)
    def validate_password(cls, value):
        if len(value) < 5:
             raise HTTPException(status_code=400, detail="Password must be atleast 5 characters long")
        return value