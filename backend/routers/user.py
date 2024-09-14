import uuid
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from models import User
from database import Session, ENGINE
from schemas import UserUpdate, UserUpdatePassword
from werkzeug.security import generate_password_hash, check_password_hash


Session = Session(bind=ENGINE)

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.get('/')
async def get_users(Authorize: AuthJWT = Depends()):
    try:
        # Authorize.jwt_required()
        users = Session.query(User).all()
        if users:
            data = {
                "status": 200,
                "message": "All users in instagram have been successfully authenticated",
                "users" : []
            }
            i = 0
            for user in users:
                i+=1
                data["users"].append({
                    "user-": i,
                    "id" : user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "created_at": user.created_at,
                })
            return jsonable_encoder(data)
        else:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Users not found")


    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")

@user_router.get('/user')
async def get_user(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        user = Session.query(User).filter(User.username == Authorize.get_jwt_subject()).first()
        data = {
            "status": 200,
            "message": f'The token you inserted belongs to the user {Authorize.get_jwt_subject()}',
            "detail" : {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "email": user.email,
                "created_at": user.created_at,
            }
        }
        return jsonable_encoder(data)
    except Exception as e:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@user_router.get('/user/{id}')
async def get_user(id: uuid.UUID):
    try:
        user = Session.query(User).filter(User.id == id).first()
        data = {
            "status": 200,
            "message": f'the user {user.username}',
            "detail" : {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "email": user.email,
                "created_at": user.created_at,
            }
        }
        return jsonable_encoder(data)
    except Exception as e:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
@user_router.put('/update-user')
async def update_user(user : UserUpdate, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        current_user = Session.query(User).filter(User.username == Authorize.get_jwt_subject()).first()
        if current_user is not None:
            for key, value in user.dict().items():
                setattr(current_user, key, value)

            Session.commit()
            data = {
                "status": 200,
                "message": "User has been successfully updated",
                "detail": {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "username": user.username,
                    "email": user.email,
                    "updated_at": user.updated_at,
                }
            }
    except Exception as e:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@user_router.put('/user-password-update')
async def user_update_password(password_update: UserUpdatePassword, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        user = Session.query(User).filter(User.username == Authorize.get_jwt_subject()).first()
        if check_password_hash(user.password, password_update.password):
            if password_update.password1 == password_update.password2:
                data = {
                    "status": 200,
                    "message": "Password has been successfully updated",
                }
                user.password = generate_password_hash(password_update.password1)
                Session.commit()
                return jsonable_encoder(data)

            else:
                return {"message": "New passwords do not match"}
        else:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User password not match")

    except Exception as e:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@user_router.delete('/delete-user')
async def delete_user(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        user = Session.query(User).filter(User.username == Authorize.get_jwt_subject()).first()
        if user:
            Session.delete(user)
            Session.commit()
            data = {
                "status": 200,
                "message": "User has been successfully deleted",
            }
            return jsonable_encoder(data)
        else:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")