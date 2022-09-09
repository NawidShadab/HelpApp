from fastapi import Body, FastAPI,Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app import oauth2
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import engine, get_db


router = APIRouter(
    prefix="/articles",
    tags=['Articles']
)


# adding new article
@router.post('/', status_code=status.HTTP_201_CREATED, )
