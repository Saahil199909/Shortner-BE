import traceback
import os

from fastapi import APIRouter, Depends, Request,  HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.constants import SHORT_LINK_DETAILS_MODELS
from app.db.database import get_db
from app.db.models import ShortLinkDetails
from app.api.redirector.utils import collect_short_link_details


project_rootpath = os.getcwd()
maxmind_db_path = os.path.join(project_rootpath, 'GeoLite2-City_20240809', 'GeoLite2-City.mmdb' )
print("Current Working Directory:", os.getcwd())
print(maxmind_db_path, "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMmm")

router = APIRouter()


@router.get('/{short_key}')
async def redirect_short_url(short_key: str, request: Request, db: Session = Depends(get_db)):
    try: 
        print(short_key, "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
        key_length = len(short_key)
        model_name = SHORT_LINK_DETAILS_MODELS.get(key_length)
        print(model_name, "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM")
        result = db.query(model_name).filter(model_name.short_key == short_key, model_name.is_deleted == False).first()
        long_url = result.long_url

        await collect_short_link_details(short_key, request, maxmind_db_path, db)

        return RedirectResponse(url=long_url)
    except Exception as e:
        error_name = type(e).__name__ 
        tb = traceback.format_exc()
        print(f"{error_name}: {e} EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE\nTraceback:\n{tb}")
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail='Unable to Redirect, plesae try again later')

