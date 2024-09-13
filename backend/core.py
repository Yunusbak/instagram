from fastapi import FastAPI
from routers.auth import auth_router
from routers.user import user_router
from routers.post import post_router
from routers.like import like_router
from routers.comment import comment_router
from api_for_tg.vector import users_tg_bot
from fastapi_jwt_auth import AuthJWT
from schemas import Settings

app = FastAPI()

@AuthJWT.load_config
def get_config():
    return Settings()
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(post_router)
app.include_router(like_router)
app.include_router(comment_router)
app.include_router(users_tg_bot)

@app.get("/")
async def root():
    return {"message" : "Welcome to Instagram Database Design"}