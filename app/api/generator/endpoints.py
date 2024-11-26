from fastapi import APIRouter, Depends,  HTTPException, status
from sqlalchemy.orm import Session

from app.constants import SHORT_LINK_DETAILS_MODELS
from app.api.generator.schemas import GeneratorSchema
from app.db.database import get_db
from app.db.models import User, FiveGenerator, SixGenerator
from app.api.generator.utils import generate_unique_string, redis_incre_counter
from app.service import RedisConnection

import asyncio

router = APIRouter()


@router.post('/')
async def generate_short_url(generator: GeneratorSchema, db: Session = Depends(get_db)):
    print(generator, "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG")
    user = db.query(User).filter(User.id == generator.user_id).first()
    if user is None:
        raise HTTPException(status_code=400, detail="User does not exist with that user id")
    try:
        print('STARTED')
        key_length = int(generator.key_length)
        print(key_length,"KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
        counter = await redis_incre_counter(key_length)
        print("after redis")
        generated_short_url = await generate_unique_string(counter, key_length)
        print('after genrating url')
        short_link_details_create = SHORT_LINK_DETAILS_MODELS.get(key_length)(short_key = generated_short_url, user_id = generator.user_id,
                                                            long_url = generator.long_url, domain = generator.domain,)
        print('after adding in generater models')
        db.add(short_link_details_create)
        db.commit()

        return {
            'short_link': f'https://{generator.domain}/{generated_short_url}'
        }
    except Exception as e:
        error_name = type(e).__name__ 
        print(f"{error_name}: {e} EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail=f"{error_name}: {e}")

    