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

@router.post('/register')
async def register(payload: UserSchema, db: Session = Depends(get_db)):
    user_obj = db.query(User).filter(User.email == payload.email).first()
    if user_obj:
        raise HTTPException(status_code=400, detail="Email already exist")
    try:
        create_user_obj = User(email = payload.email, password = payload.password)
        db.add(create_user_obj)
        db.commit()
        return {
            'user_id': create_user_obj.id,
            'msg': "User created Successfully"
        }
    except Exception as e:
        print(e)
    
