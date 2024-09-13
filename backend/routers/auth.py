import datetime
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from models import User
from schemas import UserRegister, UserLogin, Settings
from database import Session, ENGINE
from werkzeug.security import generate_password_hash, check_password_hash



Session = Session(bind=ENGINE)

auth_router = APIRouter(prefix='/auth', tags=['Authentication'])


@auth_router.post('/register')
async def register(user: UserRegister):
    check_user = Session.query(User).filter(User.username == user.username).first()
    if check_user:
        data = {
            "status": 401,
            "message": "Username already registered"
        }
        return jsonable_encoder(data)

    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
    )
    Session.add(new_user)
    Session.commit()

    hashed_user_password = new_user.password

    data = {
        "status": 201,
        "message": "User registered successfully",
        "detail" : {
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "password": hashed_user_password
        }
    }
    return jsonable_encoder(data)



@auth_router.post('/login')
async def login(user: UserLogin, Authorize : AuthJWT = Depends()):
    check_user = Session.query(User).filter(User.username == user.username).first()
    if check_user:
        if check_password_hash(check_user.password, user.password):
            access_token = Authorize.create_access_token(subject=check_user.username, expires_time=datetime.timedelta(minutes=30))
            refresh_token = Authorize.create_refresh_token(subject=check_user.username, expires_time=datetime.timedelta(hours=5))

            data = {
                "status": 200,
                "message": "Logged in successfully",
                "token":{
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }
            }
            return jsonable_encoder(data)

        else:
            data= {
                "status": 401,
                "message": "Password is incorrect"
            }
            return jsonable_encoder(data)
    else:
        data = {
            "status": 401,
            "message": "Username or password is incorrect"
        }
        return jsonable_encoder(data)




