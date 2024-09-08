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
    user = db.query(User).filter(User.id == generator.user_id).first()
    if user is None:
        raise HTTPException(status_code=400, detail="User does not exist with that user id")
    try:
        key_length = generator.key_length
        counter = await redis_incre_counter(key_length)
        generated_short_url = await generate_unique_string(counter, key_length)
        short_link_details_create = SHORT_LINK_DETAILS_MODELS.get(key_length)(short_key = generated_short_url, user_id = generator.user_id,
                                                            long_url = generator.long_url, domain = generator.domain,)
        db.add(short_link_details_create)
        db.commit()

        return {
            'short_link': f'http://{generator.domain}/{generated_short_url}'
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail='Unable to Generate Short url, plesae try again later')

    