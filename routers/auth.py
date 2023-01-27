# the fucking import error
import sys 
sys.path.append(r'E:\Mine\fastapi')

from pydantic import EmailStr
from fastapi import FastAPI, Response   , status , HTTPException , Depends , APIRouter 
from fastapi.params import Body
from database import get_db 
from schemas import UserLogin
import models
import utils , oauth2
from fastapi.security import OAuth2PasswordRequestForm
from utils import hash

from sqlalchemy.orm import Session

router = APIRouter()

# the OAuth2PasswordRequestForm is like the UserLogin schema but i dont know why we used it 
#which have the fields username and password (not email) and you need to send it from the
# form-data from postman
# and i dont know what is the Depends
#user_credentials : UserLogin  ==>> user_credentials : OAuth2PasswordRequestForm = Depends()

@router.post("/login")
def login(user_credentials : OAuth2PasswordRequestForm = Depends(),db :Session = Depends(get_db)) : 
    user = db.query(models.User).filter(models.User.email==user_credentials.username).first()
    if not user : 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="User Not Found")
    if not utils.verify(user_credentials.password ,user.password ) : 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Invalid Credentials")
    #create token 
    access_token = oauth2.create_access_token(data={"user_id" : user.id})

    #return token
    return {"accesstoken"  : access_token , "token_type" : "bearer"}

