import sys
sys.path.append(r'E:\Mine\fastapi')

import models
from schemas import UserCreate  , ResponseUser
from utils import hash
from database import get_db

from fastapi import FastAPI, Response   , status , HTTPException , Depends  , APIRouter
from fastapi.params import Body
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users" , tags=["Users"])

@router.post("/create" , response_model=ResponseUser)
def create_user(user : UserCreate = Body(...) , db : Session = Depends(get_db)): 

    
    #hashing password : encrypting it 

    hashed_password = hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user) 
    return new_user

@router.get("/get/{id}" , response_model=ResponseUser)
def get_user(id : int  , db : Session = Depends(get_db) ) : 
    user = db.query(models.User).filter(models.User.id == int(id)).first()
    if not user : 
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user 