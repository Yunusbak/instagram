import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from database import Session, ENGINE
from models import Post, User
from schemas import PostCreate, PostUpdateModel
from fastapi_jwt_auth import AuthJWT



Session = Session(bind=ENGINE)
post_router = APIRouter(prefix="/posts", tags=["posts"])

@post_router.get("/")
async def post(Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
        posts = Session.query(Post).all()
        if posts:
            data = {
                "status": "success",
                "posts": jsonable_encoder(posts)
            }
            return data
        else:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')

    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")

@post_router.get('/one-person')
async def one_person(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        check_user = Session.query(User).filter(User.username == Authorize.get_jwt_subject()).first()
        if check_user:
            posts = Session.query(Post).filter(Post.user == check_user).all()
            data = {
                "status": 200,
                "message": f"posts created by {Authorize.get_jwt_subject()}",
                "posts" : [
                    {
                        "id": post.id,
                        "user_id" : check_user.id,
                        "image_path" : post.image_path,
                        "caption" : post.caption,
                        "created_at" : post.created_at,
                    }
                    for post in posts
                ]
            }
            return jsonable_encoder(data)
        HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    except Exception as e:
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials or post not found")

@post_router.get("/{id}")
async def post(id: uuid.UUID):
    try:
        post = Session.query(Post).filter(Post.id == id).first()
        if post:
            data = {
                "status": "success",
                "post": jsonable_encoder(post)
            }
            return data
        else:
            return {"message": "post not found"}

    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")


@post_router.post("/create")
async def post(post: PostCreate, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        check_user = Session.query(User).filter(User.username == Authorize.get_jwt_subject()).first()
        if check_user:
            new_post = Post(
                user_id = check_user.id,
                image_path=post.image_path,
                caption=post.caption,
            )
            Session.add(new_post)
            Session.commit()
            data = {
                "status": 201,
                "message": "post created",
                "detail" :{
                    "user": f"Post created by {check_user.username}",
                    "image_path": new_post.image_path,
                    "caption": new_post.caption,
                    "created_at": new_post.created_at
                }
            }
            return jsonable_encoder(data)
        else:
            return HTTPException(status_code=status.HTTP_404_BAD_REQUEST, detail="User not found")

    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid token credentials or post not found')



@post_router.put("/update/{id}")
async def post(id : uuid.UUID, post: PostUpdateModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        check_user = Session.query(User).filter(User.username == Authorize.get_jwt_subject()).first()
        update_post = Session.query(Post).filter(Post.id == id).first()
        if check_user and update_post:
            for key, value in post.dict(exclude_none=True).items():
                setattr(update_post, key, value)
                Session.commit()

            data = {
                "status": 200,
                "message": "post updated",
            }
            return jsonable_encoder(data)
        else:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User or post not found")

    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid token credentials or post not found')


@post_router.delete("/delete/{id}")
async def delete(id: uuid.UUID, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        check_user = Session.query(User).filter(User.username == Authorize.get_jwt_subject()).first()
        delete_post = Session.query(Post).filter(Post.id == id).first()
        if check_user and delete_post:
            Session.delete(delete_post)
            Session.commit()
            data = {
                "status": 200,
                "message": "post deleted",
            }
            return jsonable_encoder(data)
        else:
            return {"message": "User or post not found"}

    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid token credentials or post not found')

