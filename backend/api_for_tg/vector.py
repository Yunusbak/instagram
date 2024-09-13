from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from models import User
from database import Session, ENGINE



Session = Session(bind=ENGINE)

users_tg_bot = APIRouter(prefix="/api/tg/users", tags=["tg"])

@users_tg_bot.get('/')
async def get_users():
    try:
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
                    "user": i,
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


