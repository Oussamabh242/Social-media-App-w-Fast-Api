import sys

from sqlalchemy import func
sys.path.append(r'E:\Mine\fastapi')
sys.path.append(r'E:\Mine\fastapi\routers')

import models
from schemas import Post , Response_Post
from database import get_db
from utils import hash


from fastapi import FastAPI, Response   , status , HTTPException  , APIRouter , Depends
from fastapi.params import Body
from sqlalchemy.orm import Session
from typing import List

import oauth2

router = APIRouter()

@router.get("/"  )
def all(db : Session = Depends(get_db)  , limit : int  = 10) :
    # cur.execute("""SELECT * FROM products """)
    # res = cur.fetchall()                          => psycopg2    => sqlalchemy
    posts = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).limit(limit).all()
    return posts

@router.post("/create" , response_model=Response_Post)
def create(post : Post = Body(...) , db : Session = Depends(get_db) ,user_id : int =Depends(oauth2.get_current_user)): 
    # item = item.dict()
    # item.name.capitalize()
    # edit_item = item.dict()
    # edit_item["id"] = random.randrange(0,50000)
    # items.append(edit_item)
    #  psycopg2 ====================>>>>>>>>>>>>>> sqlalchemy
    # cur.execute("""INSERT INTO products(name , price , sold) 
    # VALUES(%s , %s , %s)""" , (item["name"] , item["price"] , item["sold"]))
    # conn.commit()
    #new_post = models.Post(title = post.title , content = post.content ,published = post.published ) this not a good 
    #approch if you use a lot of information inside post so it becomes

    new_post = models.Post(**post.dict() , owner_id = user_id.id )

    db.add(new_post)
    db.commit()
    db.refresh(new_post) #get the whole columns from the pgsql db for the new post
    return new_post

@router.get("/get/{post_id}" , response_model=Response_Post)
def get_post(post_id : int , db : Session = Depends(get_db)) :
    # for i in items:
    #     if i["id"] == int(id) : #path are always interpreted as str
    #         return{"post" : i}
    
    # cur.execute(f"SELECT * FROM products WHERE id = {int(id)} ;")
    # res = cur.fetchone()
    # if res : 
    #     return {"post" : res}

    res = db.query(models.Post).filter(models.Post.id == post_id ).first()
    if res :
        return res
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@router.delete("/delete/{post_id}")
def delete(post_id : int , db : Session = Depends(get_db) , user_id : int =Depends(oauth2.get_current_user)) : 

    # cur.execute(f"SELECT * FROM products WHERE id = {int(id)} ;")
    # res = cur.fetchone()
    # if res : 
    #     cur.execute(f"DELETE FROM products WHERE id = {int(id)} ;")
    #     conn.commit()
    #     return HTTPException(status_code=status.HTTP_200_OK)
    # return HTTPException(status_code=status.HTTP_404_NOT_FOUND)


    # res = cur.fetchall() 
    # print(res)
    # for i , j in enumerate(items) : 
    #     if j["id"] == int(id) : 
    #         items.pop(i) 
    #         return Response(status_code=status.HTTP_204_NO_CONTENT)
    

    post = db.query(models.Post).filter(models.Post.id == post_id , models.Post.owner_id == user_id.id)
    if post.first()  != None: 
        post.delete(synchronize_session=False)
        db.commit()
        return {"status" : "deleted"}
    return HTTPException(status_code =status.HTTP_404_NOT_FOUND)


        
@router.put("/update/{post_id}")
def update(post_id : int , updated_post : Post , db : Session = Depends(get_db) ,user_id : int =Depends(oauth2.get_current_user)) :
    # item = item.dict()
    # for i in range(len(items)):
    #     if items[i]["id"] == int(id) : #path are always interpreted as str
    #         item["id"] = int(id)
    #         items[i] = item
    #         return Response(status_code=status.HTTP_200_OK )

    # post = post.dict()
    # cur.execute(f"SELECT * FROM products WHERE id = {int(id)} ;")
    # res = cur.fetchone()
    # if res : 
    #     cur.execute("UPDATE products SET name = %s , price = %s , sold = %s WHERE id = %s" , (item["name"] , item["price"] , item["sold"] , int(id)))
    #     conn.commit()
    #     return HTTPException(status_code=status.HTTP_200_OK)

    post_qurey = db.query(models.Post).filter(models.Post.id ==post_id )
    post = post_qurey.first()
    if post.owner_id != int(user_id.id) : 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    if post : 
        post_qurey.update(updated_post.dict() , synchronize_session=False)
        
        db.commit()
        return {"updated" : post_qurey.first()}

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND)