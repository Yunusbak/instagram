import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from database import Session, ENGINE
from models import Likes, User, Post
from schemas import LikeCreateModel


Session = Session(bind=ENGINE)


like_router = APIRouter(prefix="/likes", tags=["likes"])

@like_router.get('/')
async def get_likes(Authorize: AuthJWT = Depends()):
    try:
        current_user = Session.query(User).filter(User.username == Authorize.get_jwt_subject()).first()
        likes = Session.query(Likes).filter(Likes.user_id == current_user.id).all()
        if likes:
            data = {
                "status": "success",
                "likes": likes
            }
            return jsonable_encoder(data)
        else:
            return {"message" : "likes not found"}
    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="---")


@like_router.get('/post-like')
async def user_like_posts(Authorize: AuthJWT = Depends()): # User qaysi postlarga like bosgani
    try:
        Authorize.jwt_required()
        check_user = Session.query(User).filter(User.username == Authorize.get_jwt_subject()).first()

        if not check_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        likes = Session.query(Likes).filter(Likes.user_id == check_user.id).all()

        if likes:
            liked_posts = [Session.query(Post).filter(Post.id == like.post_id).first() for like in likes]

            data = {
                "status": 200,
                "message": f"Posts liked by {check_user.username}",
                "posts": [{
                    "id": post.id,
                    "caption": post.caption,
                    "image_path": post.image_path,
                    "created_at": post.created_at.isoformat(),
                } for post in liked_posts]
            }
            return jsonable_encoder(data)
        else:
            return {"message": "User hasn't liked any posts"}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@like_router.get("/user-like/{id}")
async def post_liked_users(id: uuid.UUID, Authorize: AuthJWT = Depends()): # ushbi postga kimlar like bosgani
    try:
        Authorize.jwt_required()
        post = Session.query(Post).filter(Post.id == id).first()

        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

        likes = Session.query(Likes).filter(Likes.post_id == post.id).all()

        if likes:
            liked_users = [Session.query(User).filter(User.id == like.user_id).first() for like in likes]

            data = {
                "status": 200,
                "message": f"Users who liked post {post.id}",
                "users": [
                    {
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name
                    }
                for user in liked_users
                ]
            }
            return jsonable_encoder(data)
        else:
            return {"message": "No users have liked this post"}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@like_router.post('/create')
async def create_like(like: LikeCreateModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        check_user = Session.query(User).filter(User.username == Authorize.get_jwt_subject()).first()
        post = Session.query(Post).filter(Post.id == like.post_id).first()
        if check_user:
            if post:
                new_like = Likes(
                    user_id=check_user.id,
                    post_id=like.post_id
                )
                Session.add(new_like)
                Session.commit()

                data = {
                    "status": 201,
                    "message": "Like added successfully",
                    "like_id": new_like.id,
                    "user": new_like.user.username,
                    "post_id":new_like.post_id
                }
                return jsonable_encoder(data)
            else:
                return {"message": "Post not found"}
        else:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@like_router.delete('/delete/{like_id}')
async def delete_like(like_id: uuid.UUID, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        current_user = Session.query(User).filter(User.username == Authorize.get_jwt_subject()).first()
        if current_user:
            like = Session.query(Likes).filter(Likes.id == like_id and Likes.user_id == current_user.id).first()
            if like:
                Session.delete(like)
                Session.commit()

                data = {
                    "status": 200,
                    "message": "Like deleted successfully",
                }
                return jsonable_encoder(data)
            else:
                return {"message": "Post likes Not found"}
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="---")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")