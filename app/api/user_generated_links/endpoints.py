from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import union_all, func, select
from sqlalchemy.orm import Session
from typing import Optional

from app.db.database import get_db
from app.db.models import User, FiveGenerator, SixGenerator, ShortLinkDetails
from app.constants import SHORT_LINK_DETAILS_MODELS
from app.api.user_generated_links.schemas import ShortlinkUpdateSchema


router = APIRouter()


@router.get('/{user_id}')
async def user_generated_links(
            user_id: int, 
            limit: Optional[int] = Query(None, description="Limit the number of records returned"),
            offset: Optional[int] = Query(None, description="Offset the starting point for records"),
            db: Session = Depends(get_db)):
    user_exist = db.query(User).filter(User.id == user_id, User.is_active == True, User.is_deleted == False).first()
    if user_exist is None:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail='User does not exist with that user id')

    # Subquery for FiveGenerator
    five_gen_select = select(
        FiveGenerator.short_key.label('short_key'),
        FiveGenerator.domain.label('domain'),
        FiveGenerator.long_url.label('long_url'),
        FiveGenerator.created_at.label('created_at')
    ).filter(FiveGenerator.user_id == user_id, FiveGenerator.is_active == True)
    
    # Subquery for SixGenerator
    six_gen_select = select(
        SixGenerator.short_key.label('short_key'),
        SixGenerator.domain.label('domain'),
        SixGenerator.long_url.label('long_url'),
        SixGenerator.created_at.label('created_at')
    ).filter(SixGenerator.user_id == user_id, SixGenerator.is_active == True)
    
    # Combine subqueries using UNION ALL
    combined_subquery = union_all(five_gen_select, six_gen_select).alias('combined_urls')
    
    # Count occurrences in ShortLinkDetails
    count_query = select(
        combined_subquery.c.short_key,
        func.count(ShortLinkDetails.short_key).label('count')
    ).outerjoin(
        ShortLinkDetails, combined_subquery.c.short_key == ShortLinkDetails.short_key
    ).group_by(
        combined_subquery.c.short_key
    ).alias('count_query')

    # Final query to get URL details and count
    final_query = select(
        combined_subquery.c.short_key,
        combined_subquery.c.domain,
        combined_subquery.c.long_url,
        combined_subquery.c.created_at,
        count_query.c.count
    ).join(
        count_query, combined_subquery.c.short_key == count_query.c.short_key
    )

    total_count = db.execute(select(func.count()).select_from(final_query.subquery())).scalar()

    final_query = final_query.order_by(combined_subquery.c.created_at.desc()).limit(limit).offset(offset)

    result = db.execute(final_query).fetchall()
    response_list = [] 
    for i in result:
        data = {
            'short_key' : f'http://{i.domain}/{i.short_key}',
            'long_url' : i.long_url,
            'created_at' : i.created_at.date(),
            'clicks_count' : i.count
        }
        response_list.append(data)
    return {
        'total_data' : total_count,
        'data' : response_list
    }



@router.get('/short-key/{short_key}')
async def short_link_detail(short_key: str, db: Session = Depends(get_db)):
    short_key_length = len(short_key) 
    model_name = SHORT_LINK_DETAILS_MODELS.get(short_key_length)
    short_link_exist = db.query(model_name).filter(model_name.short_key == short_key, model_name.is_active == True).first()
    if short_link_exist is None:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail='Short key is not present in db')
    return {
        'short_key' : short_link_exist.short_key,
        'long_url' : short_link_exist.long_url,
        'domain' : short_link_exist.domain, 
    }


@router.put('/short-key/{short_key}')
async def update_short_link(short_key: str, shortlink_update_payload: ShortlinkUpdateSchema, db: Session = Depends(get_db)):
    try:
        short_key_length = len(short_key) 
        model_name = SHORT_LINK_DETAILS_MODELS.get(short_key_length)
        short_link_exist = db.query(model_name).filter(model_name.short_key == short_key, model_name.is_active == True).first()
        if short_link_exist is None:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail='Short key is not present in db or is deleted')
        short_link_exist.long_url = shortlink_update_payload.long_url
        db.commit()
        return {'msg' : 'Details updated Succesfully'}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to update. Please try again later.")


@router.delete('/short-key/{short_key}')
async def delete_short_link(short_key: str, db: Session = Depends(get_db)):
    short_key_length = len(short_key) 
    model_name = SHORT_LINK_DETAILS_MODELS.get(short_key_length)
    short_link_exist = db.query(model_name).filter(model_name.short_key == short_key, model_name.is_active == True).first()
    if short_link_exist is None:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail='Short key is not present in db')
    try:
        short_link_exist.is_active = False
        short_link_exist.is_deleted = True
        short_link_exist.updated_at = datetime.now()
        db.commit()
        return {'msg' : f'{short_key} deleted succesfully'}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to delete. Please try again later.")
   





    
