import sys
sys.path.append(r'E:\Mine\fastapi')

import models
from schemas import UserCreate  , ResponseUser , TokenData ,Vote
from utils import hash
from database import get_db
import oauth2

from fastapi import FastAPI, Response   , status , HTTPException , Depends  , APIRouter
from fastapi.params import Body
from sqlalchemy.orm import Session
from utils import hash


router = APIRouter(prefix="/vote" , tags=["vote"])

@router.post("/")
def voting(vote : Vote ,db : Session = Depends(get_db) ,user : TokenData =  Depends(oauth2.get_current_user) ) : 
    votes = db.query(models.Votes).filter(models.Votes.user_id == user.id , models.Votes.post_id == vote.post_id)


    if vote.dir == 1: 
        if votes.first() == None : 
            new_vote = models.Votes(user_id = user.id , post_id = vote.post_id )
            db.add(new_vote)
            db.commit()
            db.refresh(new_vote)

            return new_vote
        else : 
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    else : 
        if votes.first() != None : 
            if votes  != None: 
                votes.delete(synchronize_session=False)
                db.commit()
                return {"status" : "deleted"}
    return HTTPException(status_code= status.HTTP_400_BAD_REQUEST)


    


