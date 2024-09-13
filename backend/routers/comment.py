import uuid
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_jwt_auth import AuthJWT
from database import Session, ENGINE
from fastapi.encoders import jsonable_encoder
from models import User, Comments, Post
from schemas import CommentCreateSchema, CommentUpdateSchema

Session = Session(bind=ENGINE)

comment_router = APIRouter(prefix="/comments", tags=["comments"])

@comment_router.get("/user-comments")
async def get_user_comments(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        current_user = Session.query(User).filter(User.username == Authorize.get_jwt_subject()).first()
        comments = Session.query(Comments).filter(Comments.user_id == current_user.id).all()
        if current_user:
            if comments:
                data = {
                    "status": 200,
                    "message": f"These comments are from the user {current_user.username}",
                    "comments": comments
                }
                return jsonable_encoder(data)
            else:
                return {"message": "comments not found"}
        return {"message": "user not found"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")


@comment_router.get("/post-comments/{id}")
async def get_post_comments(id: uuid.UUID, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        post = Session.query(Post).filter(Post.id == id).first()
        if post:
            comments = Session.query(Comments).filter(Comments.post_id == post.id).all()
            if comments:
                users_comments = []
                for comment in comments:
                    user = Session.query(User).filter(User.id == comment.user_id).first()
                    if user:
                        users_comments.append({
                            "username": user.username,
                            "comment": comment.content
                        })

                data = {
                    "status": 200,
                    "message": f"This post was commented on by {len(users_comments)} users",
                    "comments": users_comments
                }
                return jsonable_encoder(data)
            else:
                return {"message": "No comments found for this post"}
        return {"message": "Post not found"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")


@comment_router.post("/create-comment/{id}")
async def comment_create(id: uuid.UUID, comment : CommentCreateSchema, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        post = Session.query(Post).filter(Post.id == id).first()
        current_user = Session.query(User).filter(User.username == Authorize.get_jwt_subject()).first()

        if current_user:
            if post:
                new_comment = Comments(
                    user_id=current_user.id,
                    post_id=post.id,
                    content=comment.content,
                )
                Session.add(new_comment)
                Session.commit()

                data = {
                    "status": 200,
                    "message": f"Comment successfully created by {current_user.username} and content -- {new_comment.content}",
                }
                return jsonable_encoder(data)
        return {"message": "user or post not found"}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")

@comment_router.put("/update-comment/{id}")
async def update_user_comment(id : uuid.UUID, comment : CommentUpdateSchema, Authorize: AuthJWT = Depends()):
    try:
        current_user = Session.query(User).filter(User.username == Authorize.get_jwt_subject()).first()
        comment_id = Session.query(Comments).filter(Comments.id == id).first()
        if current_user:
            if comment_id:
                for key, value in comment.dict(exclude_none=True).items():
                    setattr(comment_id, key, value)
                    Session.commit()

                data = {
                    "status": 200,
                    "message": f"Comment successfully updated by {current_user.username}",
                }
                return jsonable_encoder(data)

        return {"message": "user or comment not found"}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")


@comment_router.delete("/delete-comment/{id}")
async def delete_comment(id: uuid.UUID, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        current_user = Session.query(User).filter(User.username == Authorize.get_jwt_subject()).first()
        comment_id = Session.query(Comments).filter(Comments.id == id).first()
        if comment_id:
            Session.delete(comment_id)
            Session.commit()
            data = {
                "status": 200,
                "message": f"Comment successfully deleted by {current_user.username}",
            }
            return jsonable_encoder(data)
        else:
            return {"message": "comment not found"}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")