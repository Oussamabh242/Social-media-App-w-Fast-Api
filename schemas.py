import sys 
sys.path.append(r'E:\Mine\fastapi')

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from fastapi import Depends
from database import get_db
from sqlalchemy.orm import Session
import models
import psycopg2

def get_user(owner_id) : 
    conn = psycopg2.connect("dbname=FastAPI user=postgres password=oussama.bh")

    #Creating cursor 
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users WHERE users.id = {owner_id} ")
    res = cur.fetchone()
    return res


class Post(BaseModel) : 
    title : str
    content : str
    published : bool = True




class UserCreate(BaseModel) : 
    email :str
    password : str

class ResponseUser(BaseModel) : 
    email : str 
    created_at : datetime
    class Config : 
        orm_mode = True

class UserLogin(BaseModel) : 
    email : EmailStr
    password : str

class Token(BaseModel) :
    access_token : str
    token_type : str


class TokenData(BaseModel): 
    id : Optional[str] = None

class Vote(BaseModel): 
    post_id : int
    dir : conint(le=1)

class Response_Post(Post) : 
    title : str 
    content : str 
    published : bool
    created_at : datetime
    owner_id : int

    class Config : 
        orm_mode = True  
    # the respose is by default dealing with dictionaries so with config we let it uses the orm ...
class OutPost(Response_Post) :
    Post : Response_Post
    votes : int