import os
import uuid
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
load_dotenv()

#
class Settings(BaseModel):
    authjwt_secret_key : str=os.getenv('authjwt_secret_key')


# User Register #

class UserRegister(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    username: Optional[str]

class UserLogin(BaseModel):
    username : Optional[str]
    password: Optional[str]

class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    email: Optional[str]
    updated_at: Optional[str]

class UserUpdatePassword(BaseModel):
    password: Optional[str]
    password1: Optional[str]
    password2: Optional[str]




# Post #
class PostCreate(BaseModel):
    image_path: Optional[str]
    caption: Optional[str]

class PostUpdateModel(BaseModel):
    caption: Optional[str]
    image_path: Optional[str]


# Like #

class LikeCreateModel(BaseModel):
    post_id : Optional[uuid.UUID]


# Comment #

class CommentCreateSchema(BaseModel):
    post_id : Optional[uuid.UUID]
    content: Optional[str]

class CommentUpdateSchema(BaseModel):
    content: Optional[str]