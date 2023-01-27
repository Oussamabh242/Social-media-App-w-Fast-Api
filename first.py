#the fucking import error
import sys
sys.path.append(r'.')
sys.path.append(r'.\routers')



from fastapi import FastAPI, Response   , status , HTTPException , Depends
from enum import Enum
from database import SessionLocal, engine ,Base , get_db
import models , config
from sqlalchemy.orm import Session
from routers import post , user , auth , vote

models.Base.metadata.create_all(bind=engine)


#connecting to database 
# conn = psycopg2.connect("dbname=FastAPI user=postgres password=oussama.bh")

# #Creating cursor 
# cur = conn.cursor()



#in order to create fixed url or like specifing the type of a variable like using a : int it becomes
# a : fixed_urls => wich is the varaible a's type
class fixed_urls(str , Enum) : 
    home = "home"
    profile = "profile"
    login = "login"




Posts = [    {        "name": "Post1",        "description": "This is Post 1",        "price": 10.5,        "tax": 1.5,        "id": 1    },    {        "name": "Post2",        "description": "This is Post 2",        "price": 20.0,        "tax": 2.0,        "id": 2    },    {        "name": "Post3",        "description": "This is Post 3",        "price": 15.75,        "tax": 2.25,        "id": 3    }]



app = FastAPI()


app.include_router(post.router , prefix="/posts" , tags=["Posts"])
app.include_router(user.router)
app.include_router(auth.router,prefix="/auth" , tags=["Authentication"])
app.include_router(vote.router)

@app.get("/")
def hello_world() : 
    return {"message" : "hello world"}



@app.get("/wtf/{model_name}")
def wsup(model_name : fixed_urls) : 
    if model_name == fixed_urls.home : 
        return {"message" : "welcome to the home page"}
    if model_name.value == "login" : 
        return {"message" : "welcome to the login page"}
    else : 
        return {"message" : "welcome to your profile"}


