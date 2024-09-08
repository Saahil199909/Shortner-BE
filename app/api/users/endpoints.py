from fastapi import APIRouter, Depends,  HTTPException
from sqlalchemy.orm import Session

from app.api.users.schemas import UserSchema
from app.db.database import get_db
from app.db.models import User

router = APIRouter()

@router.post('/')
async def login(user: UserSchema, db: Session = Depends(get_db)):
    result = db.query(User).filter(User.email == user.email).first()
    if result is None:
        raise HTTPException(status_code=400, detail="Email does not exist")
    if result.password != user.password:
        raise HTTPException(status_code=400, detail="Email and password does not match")
    return{
        'user_id': result.id,
        'msg': 'Login successfull'
    }